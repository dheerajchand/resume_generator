#!/bin/bash

# Resume Generator Installation Script
# This script installs the Resume Generator system on Unix-like systems (Mac, Linux)

set -e  # Exit on any error

echo "🚀 Resume Generator Installation Script"
echo "======================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
check_python() {
    print_status "Checking Python installation..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
        print_success "Python 3 is installed: $PYTHON_VERSION"
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
        if [[ $PYTHON_VERSION == 3.* ]]; then
            print_success "Python 3 is installed: $PYTHON_VERSION"
            PYTHON_CMD="python"
        else
            print_error "Python 2 is installed, but Python 3 is required"
            exit 1
        fi
    else
        print_error "Python is not installed. Please install Python 3.11 or newer."
        echo "Download from: https://www.python.org/downloads/"
        exit 1
    fi
}

# Check if pip is installed
check_pip() {
    print_status "Checking pip installation..."
    
    if command -v pip3 &> /dev/null; then
        print_success "pip3 is available"
        PIP_CMD="pip3"
    elif command -v pip &> /dev/null; then
        print_success "pip is available"
        PIP_CMD="pip"
    else
        print_warning "pip is not installed. Installing pip..."
        $PYTHON_CMD -m ensurepip --upgrade
        PIP_CMD="$PYTHON_CMD -m pip"
    fi
}

# Create virtual environment
create_venv() {
    print_status "Creating virtual environment..."
    
    if [ -d "venv" ]; then
        print_warning "Virtual environment already exists. Removing old one..."
        rm -rf venv
    fi
    
    $PYTHON_CMD -m venv venv
    print_success "Virtual environment created"
}

# Activate virtual environment
activate_venv() {
    print_status "Activating virtual environment..."
    
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        print_success "Virtual environment activated"
    else
        print_error "Failed to activate virtual environment"
        exit 1
    fi
}

# Install dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt not found. Are you in the right directory?"
        exit 1
    fi
    
    pip install -r requirements.txt
    print_success "Dependencies installed"
}

# Set up database
setup_database() {
    print_status "Setting up database..."
    
    $PYTHON_CMD manage.py migrate
    print_success "Database migrations completed"
    
    print_status "Setting up system data..."
    $PYTHON_CMD manage.py setup_resume_system --create-superuser
    print_success "System data created"
}

# Create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    
    mkdir -p media/generated_resumes
    mkdir -p logs
    mkdir -p temp
    mkdir -p content/role_overrides
    
    print_success "Directories created"
}

# Set permissions
set_permissions() {
    print_status "Setting file permissions..."
    
    chmod +x manage.py
    chmod -R 755 .
    
    print_success "Permissions set"
}

# Test installation
test_installation() {
    print_status "Testing installation..."
    
    # Test Django
    $PYTHON_CMD manage.py check
    print_success "Django configuration is valid"
    
    # Test database
    $PYTHON_CMD manage.py shell -c "from django.contrib.auth.models import User; print('Users:', User.objects.count())"
    print_success "Database is working"
    
    print_success "Installation test passed"
}

# Print success message
print_success_message() {
    echo ""
    echo "🎉 Installation Complete!"
    echo "========================"
    echo ""
    echo "Your Resume Generator is ready to use!"
    echo ""
    echo "Next steps:"
    echo "1. Start the server:"
    echo "   source venv/bin/activate"
    echo "   python manage.py runserver"
    echo ""
    echo "2. Open your browser:"
    echo "   http://127.0.0.1:8000/"
    echo ""
    echo "3. Login with:"
    echo "   Username: admin"
    echo "   Password: admin123"
    echo ""
    echo "4. Start creating resumes!"
    echo ""
    echo "For help, check the documentation in the docs/ folder"
    echo ""
}

# Main installation process
main() {
    echo "Starting installation process..."
    echo ""
    
    check_python
    check_pip
    create_venv
    activate_venv
    install_dependencies
    create_directories
    setup_database
    set_permissions
    test_installation
    print_success_message
}

# Run main function
main "$@"
