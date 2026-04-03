#!/bin/bash
# MiniMax Agent Deployment Script

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         MiniMax Agent - Deployment Script v1.0            ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Configuration
DEPLOY_DIR="${DEPLOY_DIR:-/opt/mmagent}"
BACKUP_DIR="/tmp/mmagent-backup-$(date +%Y%m%d-%H%M%S)"
FRONTEND_DIST="frontend/dist"
API_PORT="${API_PORT:-8000}"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_requirements() {
    log_info "Checking requirements..."

    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        exit 1
    fi

    # Check docker-compose
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        log_error "Docker Compose is not installed"
        exit 1
    fi

    log_success "All requirements met"
}

backup_existing() {
    if [ -d "$DEPLOY_DIR" ]; then
        log_info "Backing up existing deployment to $BACKUP_DIR"
        mkdir -p "$BACKUP_DIR"
        cp -r "$DEPLOY_DIR"/* "$BACKUP_DIR/" 2>/dev/null || true
        log_success "Backup created"
    fi
}

build_images() {
    log_info "Building Docker images..."

    cd "$(dirname "$0")/.."

    docker build \
        -t mmagent:latest \
        -f docker/Dockerfile \
        .

    log_success "Images built successfully"
}

deploy() {
    log_info "Deploying MiniMax Agent..."

    cd "$(dirname "$0")/.."

    # Create deployment directory
    mkdir -p "$DEPLOY_DIR"

    # Copy files
    cp -r . "$DEPLOY_DIR/"

    # Create environment file
    cat > "$DEPLOY_DIR/.env" << EOF
LLM_GATEWAY_BASE_URL=${LLM_GATEWAY_BASE_URL:-http://10.138.255.202:8080}
ANTHROPIC_BASE_URL=${ANTHROPIC_BASE_URL:-http://127.0.0.1:8765}
API_HOST=0.0.0.0
API_PORT=$API_PORT
DEBUG=false
EOF

    # Start services
    cd "$DEPLOY_DIR"

    if command -v docker-compose &> /dev/null; then
        docker-compose up -d
    else
        docker compose up -d
    fi

    log_success "Deployment complete!"
}

verify() {
    log_info "Verifying deployment..."

    sleep 5

    # Check API health
    if curl -sf "http://localhost:$API_PORT/api/health" > /dev/null; then
        log_success "API is healthy"
    else
        log_warning "API health check failed - may still be starting"
    fi

    # Check containers
    log_info "Running containers:"
    docker ps --filter "name=mmagent" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
}

rollback() {
    log_warning "Rolling back to backup..."

    if [ -d "$BACKUP_DIR" ]; then
        rm -rf "$DEPLOY_DIR"
        mkdir -p "$DEPLOY_DIR"
        cp -r "$BACKUP_DIR"/* "$DEPLOY_DIR/"

        cd "$DEPLOY_DIR"
        docker-compose restart

        log_success "Rollback complete"
    else
        log_error "No backup found"
    fi
}

show_status() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}                  MiniMax Agent Status                      ${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo ""

    # API Status
    echo -e "${GREEN}API Status:${NC}"
    curl -s "http://localhost:$API_PORT/api/health" | python3 -m json.tool 2>/dev/null || echo "API not responding"
    echo ""

    # Container Status
    echo -e "${GREEN}Containers:${NC}"
    docker ps --filter "name=mmagent" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    echo ""

    # Endpoints
    echo -e "${GREEN}Available Endpoints:${NC}"
    echo "  - API:       http://localhost:$API_PORT"
    echo "  - Docs:      http://localhost:$API_PORT/docs"
    echo "  - Health:    http://localhost:$API_PORT/api/health"
    echo ""
}

usage() {
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  deploy     Deploy MiniMax Agent"
    echo "  build      Build Docker images"
    echo "  verify     Verify deployment"
    echo "  rollback   Rollback to previous version"
    echo "  status     Show deployment status"
    echo "  stop       Stop services"
    echo "  restart    Restart services"
    echo ""
}

# Main
case "${1:-deploy}" in
    deploy)
        check_requirements
        backup_existing
        build_images
        deploy
        verify
        show_status
        ;;
    build)
        check_requirements
        build_images
        ;;
    verify)
        verify
        ;;
    rollback)
        rollback
        ;;
    status)
        show_status
        ;;
    stop)
        cd "$(dirname "$0")/.."
        docker-compose down 2>/dev/null || docker compose down
        log_success "Services stopped"
        ;;
    restart)
        cd "$(dirname "$0")/.."
        docker-compose restart 2>/dev/null || docker compose restart
        log_success "Services restarted"
        ;;
    *)
        usage
        exit 1
        ;;
esac

echo ""
log_success "Done!"
