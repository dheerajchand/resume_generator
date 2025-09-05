# Getting Started Guide

## 🎯 What This Guide Does

This guide will take you from having nothing to having a working resume generator system. No technical knowledge required!

## 📋 What You'll Need

### 1. A Computer
- **Windows**: Windows 10 or newer
- **Mac**: macOS 10.14 or newer  
- **Linux**: Ubuntu 18.04 or newer (or similar)

### 2. Internet Connection
- To download the software
- To access the web interface

### 3. About 30 Minutes
- 15 minutes to install
- 15 minutes to create your first resume

## 🚀 Step 1: Install Python

### What is Python?
Python is a programming language that our resume generator needs to run. Don't worry - you don't need to learn programming!

### Windows Users

1. **Go to**: https://www.python.org/downloads/
2. **Click**: "Download Python 3.11" (or latest version)
3. **Run the installer**:
   - ✅ **IMPORTANT**: Check "Add Python to PATH"
   - Click "Install Now"
   - Wait for it to finish

### Mac Users

1. **Open Terminal** (Press Cmd+Space, type "Terminal", press Enter)
2. **Install Homebrew** (if you don't have it):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. **Install Python**:
   ```bash
   brew install python
   ```

### Linux Users

1. **Open Terminal**
2. **Run this command**:
   ```bash
   sudo apt update && sudo apt install python3 python3-pip
   ```

### ✅ Verify Python is Installed

1. **Open Terminal/Command Prompt**
2. **Type**: `python --version`
3. **You should see**: `Python 3.11.x` (or similar)

If you see an error, Python isn't installed correctly. Go back to the installation steps.

## 🚀 Step 2: Download the Resume Generator

### Option A: Download from GitHub (Recommended)

1. **Go to**: https://github.com/your-username/resume-generator
2. **Click**: Green "Code" button
3. **Click**: "Download ZIP"
4. **Extract** the ZIP file to your Desktop
5. **Rename** the folder to `resume-generator`

### Option B: Clone with Git (If you have Git)

1. **Open Terminal/Command Prompt**
2. **Navigate to where you want the project**:
   ```bash
   cd Desktop
   ```
3. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/resume-generator.git
   ```

## 🚀 Step 3: Install Dependencies

### What are Dependencies?
Dependencies are other pieces of software that our resume generator needs to work. Think of them like ingredients in a recipe.

### Install Steps

1. **Open Terminal/Command Prompt**
2. **Navigate to the project folder**:
   ```bash
   cd Desktop/resume-generator
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### ⚠️ If You Get Errors

**Error: "pip is not recognized"**
- **Solution**: Use `python -m pip install -r requirements.txt` instead

**Error: "Permission denied"**
- **Solution**: Add `--user` at the end: `pip install -r requirements.txt --user`

**Error: "No module named pip"**
- **Solution**: Install pip first: `python -m ensurepip --upgrade`

## 🚀 Step 4: Set Up the Database

### What is a Database?
A database is like a digital filing cabinet that stores all your resume data.

### Set Up Steps

1. **Make sure you're in the project folder**:
   ```bash
   cd Desktop/resume-generator
   ```

2. **Create the database**:
   ```bash
   python manage.py migrate
   ```

3. **Set up the system**:
   ```bash
   python manage.py setup_resume_system --create-superuser
   ```

### What This Does
- Creates a database file (`db.sqlite3`)
- Sets up 8 resume templates
- Creates 3 color schemes
- Sets up 50+ skills
- Creates an admin account

## 🚀 Step 5: Start the Server

### What is a Server?
A server is like a waiter in a restaurant - it takes your requests and brings you what you need. In this case, it serves your resume generator website.

### Start the Server

1. **Make sure you're in the project folder**:
   ```bash
   cd Desktop/resume-generator
   ```

2. **Start the server**:
   ```bash
   python manage.py runserver
   ```

3. **You should see**:
   ```
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CTRL+C
   ```

### ✅ Success!
Your resume generator is now running! 🎉

## 🚀 Step 6: Access the Website

### Open Your Browser

1. **Open any web browser** (Chrome, Firefox, Safari, Edge)
2. **Go to**: http://127.0.0.1:8000/
3. **You should see**: The resume generator homepage

### Login to Admin

1. **Go to**: http://127.0.0.1:8000/admin/
2. **Username**: `admin`
3. **Password**: `admin123`
4. **Click**: "Log in"

## 🚀 Step 7: Create Your First Resume

### Quick Start

1. **Go to**: http://127.0.0.1:8000/
2. **Click**: "Create New Resume"
3. **Fill in your information**:
   - Name: Your full name
   - Email: Your email address
   - Phone: Your phone number
   - Location: Your city, state
4. **Choose a template**: Pick one that matches your field
5. **Click**: "Generate Resume"
6. **Download**: Your resume in PDF, DOCX, or RTF format

### 🎉 Congratulations!
You've successfully set up and used the resume generator!

## 🔧 Troubleshooting

### Common Problems

**Problem**: "python is not recognized"
- **Solution**: Python isn't installed or not in PATH. Reinstall Python and check "Add Python to PATH"

**Problem**: "No module named django"
- **Solution**: Dependencies aren't installed. Run `pip install -r requirements.txt`

**Problem**: "Port 8000 is already in use"
- **Solution**: Stop other programs using port 8000, or use a different port: `python manage.py runserver 8001`

**Problem**: "Database is locked"
- **Solution**: Close any other programs that might be using the database, then try again

**Problem**: Website won't load
- **Solution**: Make sure the server is running and you're using the correct URL

### Still Stuck?

1. **Check the [Troubleshooting Guide](troubleshooting.md)**
2. **Read the [FAQ](faq.md)**
3. **Create an issue on GitHub**
4. **Email support**: support@resumegenerator.com

## 📚 Next Steps

Now that you have the system running:

1. **Read the [User Manual](user-manual.md)** - Learn how to use all features
2. **Check out [Examples](examples.md)** - See real resume examples
3. **Watch [Video Tutorials](video-tutorials.md)** - Step-by-step videos
4. **Explore [Developer Guide](developer-guide.md)** - If you want to customize

## 🎯 Summary

You've successfully:
- ✅ Installed Python
- ✅ Downloaded the resume generator
- ✅ Installed all dependencies
- ✅ Set up the database
- ✅ Started the server
- ✅ Accessed the website
- ✅ Created your first resume

**The system is now ready to use!** 🚀

---

**Remember**: If you get stuck at any step, it's not your fault. The documentation should be clearer. Let us know what's confusing!
