# Troubleshooting Guide

## 🚨 Common Problems and Solutions

This guide helps you fix common issues with the Resume Generator system. Most problems have simple solutions!

## 🔧 Installation Issues

### Problem: "python is not recognized"

**What it means**: Your computer can't find Python.

**Solutions**:
1. **Reinstall Python**:
   - Download from https://www.python.org/downloads/
   - ✅ **IMPORTANT**: Check "Add Python to PATH" during installation
   - Restart your computer after installation

2. **Add Python to PATH manually**:
   - **Windows**: Add `C:\Python311` and `C:\Python311\Scripts` to your PATH
   - **Mac/Linux**: Add `/usr/local/bin/python3` to your PATH

3. **Use full path**:
   ```bash
   C:\Python311\python.exe --version
   ```

### Problem: "pip is not recognized"

**What it means**: Python is installed but pip (package installer) is missing.

**Solutions**:
1. **Install pip**:
   ```bash
   python -m ensurepip --upgrade
   ```

2. **Use python -m pip**:
   ```bash
   python -m pip install -r requirements.txt
   ```

3. **Reinstall Python**: Make sure to check "Add Python to PATH"

### Problem: "Permission denied" when installing packages

**What it means**: Your user doesn't have permission to install packages.

**Solutions**:
1. **Use --user flag**:
   ```bash
   pip install -r requirements.txt --user
   ```

2. **Run as administrator** (Windows):
   - Right-click Command Prompt
   - Select "Run as administrator"
   - Try again

3. **Use virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Problem: "No module named django"

**What it means**: Django isn't installed.

**Solutions**:
1. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Check if you're in the right directory**:
   ```bash
   ls requirements.txt  # Should show the file
   ```

3. **Use virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## 🗄️ Database Issues

### Problem: "Database is locked"

**What it means**: Another process is using the database.

**Solutions**:
1. **Close other programs** that might be using the database
2. **Restart your computer**
3. **Delete the database and recreate**:
   ```bash
   rm db.sqlite3
   python manage.py migrate
   python manage.py setup_resume_system --create-superuser
   ```

### Problem: "No such table" errors

**What it means**: Database tables don't exist.

**Solutions**:
1. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

2. **Set up the system**:
   ```bash
   python manage.py setup_resume_system --create-superuser
   ```

### Problem: "Migration conflicts"

**What it means**: Database migrations are out of sync.

**Solutions**:
1. **Reset database**:
   ```bash
   rm db.sqlite3
   python manage.py migrate
   python manage.py setup_resume_system --create-superuser
   ```

2. **Fake migrations** (advanced):
   ```bash
   python manage.py migrate --fake-initial
   ```

## 🌐 Server Issues

### Problem: "Port 8000 is already in use"

**What it means**: Another program is using port 8000.

**Solutions**:
1. **Use a different port**:
   ```bash
   python manage.py runserver 8001
   ```
   Then go to http://127.0.0.1:8001/

2. **Find and stop the other program**:
   ```bash
   # Find what's using port 8000
   lsof -i :8000  # Mac/Linux
   netstat -ano | findstr :8000  # Windows
   
   # Kill the process
   kill -9 <process_id>  # Mac/Linux
   taskkill /PID <process_id> /F  # Windows
   ```

3. **Restart your computer**

### Problem: "Website won't load"

**What it means**: The server isn't running or there's a connection issue.

**Solutions**:
1. **Check if server is running**:
   - Look for "Starting development server at http://127.0.0.1:8000/"
   - If not, start it: `python manage.py runserver`

2. **Check the URL**:
   - Use http://127.0.0.1:8000/ (not https)
   - Make sure there's no typo

3. **Check firewall**:
   - Windows: Allow Python through Windows Firewall
   - Mac: Check System Preferences > Security & Privacy
   - Linux: Check iptables or ufw settings

4. **Try different browser**:
   - Chrome, Firefox, Safari, Edge

### Problem: "Internal Server Error"

**What it means**: There's a bug in the code.

**Solutions**:
1. **Check the terminal** for error messages
2. **Restart the server**:
   ```bash
   # Stop server (Ctrl+C)
   python manage.py runserver
   ```

3. **Check database**:
   ```bash
   python manage.py migrate
   ```

4. **Reset everything**:
   ```bash
   rm db.sqlite3
   python manage.py migrate
   python manage.py setup_resume_system --create-superuser
   python manage.py runserver
   ```

## 📄 File Generation Issues

### Problem: "Resume won't generate"

**What it means**: There's an issue with the resume generation process.

**Solutions**:
1. **Check required fields**:
   - Make sure personal information is filled
   - Add at least one experience or project
   - Check that summary is not empty

2. **Check for placeholders**:
   - Don't use "Your Name", "Your Company", etc.
   - Use real information

3. **Try different template**:
   - Some templates might have issues
   - Try a different role or version

4. **Check file permissions**:
   ```bash
   chmod 755 .  # Make sure directory is writable
   ```

### Problem: "Generated file is empty or corrupted"

**What it means**: The file generation process failed.

**Solutions**:
1. **Check content**:
   - Make sure all required fields are filled
   - Avoid special characters that might cause issues

2. **Try different format**:
   - If PDF fails, try DOCX
   - If DOCX fails, try RTF

3. **Check disk space**:
   ```bash
   df -h .  # Check available space
   ```

4. **Restart server**:
   ```bash
   # Stop server (Ctrl+C)
   python manage.py runserver
   ```

### Problem: "Can't download files"

**What it means**: File download is not working.

**Solutions**:
1. **Check browser settings**:
   - Allow downloads
   - Check download folder permissions

2. **Try different browser**:
   - Some browsers block downloads

3. **Check file exists**:
   - Look in the media/generated_resumes/ folder
   - Make sure file was actually created

4. **Clear browser cache**:
   - Clear cookies and cache
   - Try incognito/private mode

## 🔐 Authentication Issues

### Problem: "Can't log in"

**What it means**: Login credentials are wrong or account doesn't exist.

**Solutions**:
1. **Check credentials**:
   - Username: `admin`
   - Password: `admin123`

2. **Create new superuser**:
   ```bash
   python manage.py createsuperuser
   ```

3. **Reset password**:
   ```bash
   python manage.py changepassword admin
   ```

4. **Check if user exists**:
   ```bash
   python manage.py shell
   >>> from django.contrib.auth.models import User
   >>> User.objects.all()
   ```

### Problem: "Access denied" errors

**What it means**: You don't have permission to access a resource.

**Solutions**:
1. **Log in first**:
   - Go to http://127.0.0.1:8000/admin/
   - Log in with admin credentials

2. **Check user permissions**:
   - Make sure you're logged in
   - Check if your account has the right permissions

3. **Clear browser data**:
   - Clear cookies and cache
   - Try incognito/private mode

## 🐛 Content Issues

### Problem: "Content looks wrong"

**What it means**: The resume content is not displaying correctly.

**Solutions**:
1. **Use preview function**:
   - Click "Preview Resume" before generating
   - Check how content looks

2. **Check for special characters**:
   - Avoid characters like &, <, >, "
   - Use plain text when possible

3. **Try different template**:
   - Some templates handle content differently
   - Try a different role or version

4. **Check content length**:
   - Very long content might not fit
   - Try shorter descriptions

### Problem: "Placeholders in resume"

**What it means**: The system is showing placeholder text instead of real content.

**Solutions**:
1. **Fill in all required fields**:
   - Personal information
   - Experience
   - Projects
   - Education

2. **Check for placeholder text**:
   - Don't use "Your Name", "Your Company", etc.
   - Use real information

3. **Use the validation system**:
   - The system should warn you about placeholders
   - Fix any warnings before generating

## 🔧 Performance Issues

### Problem: "System is slow"

**What it means**: The system is running slowly.

**Solutions**:
1. **Close other programs**:
   - Free up memory and CPU
   - Close unnecessary browser tabs

2. **Check system resources**:
   - Make sure you have enough RAM
   - Check CPU usage

3. **Restart the server**:
   ```bash
   # Stop server (Ctrl+C)
   python manage.py runserver
   ```

4. **Clear temporary files**:
   ```bash
   rm -rf temp/
   rm -rf __pycache__/
   ```

### Problem: "Memory errors"

**What it means**: The system is running out of memory.

**Solutions**:
1. **Close other programs**:
   - Free up memory
   - Close unnecessary browser tabs

2. **Restart your computer**:
   - Clear all memory
   - Start fresh

3. **Check system requirements**:
   - Make sure you have enough RAM
   - Consider upgrading if needed

## 🆘 Getting Help

### Before Asking for Help

1. **Check this guide** - Your problem might be listed here
2. **Restart everything** - Server, browser, computer
3. **Check the terminal** - Look for error messages
4. **Try a different approach** - Different browser, different method

### When Asking for Help

Include this information:

1. **What you were trying to do**
2. **What error message you got** (copy and paste)
3. **What you've already tried**
4. **Your operating system** (Windows, Mac, Linux)
5. **Python version** (`python --version`)
6. **Screenshot** if helpful

### Where to Get Help

1. **GitHub Issues**: https://github.com/your-repo/issues
2. **Email**: support@resumegenerator.com
3. **Documentation**: This guide and others in `/docs`

### Emergency Reset

If nothing else works, reset everything:

```bash
# 1. Stop the server (Ctrl+C)

# 2. Delete everything
rm -rf db.sqlite3
rm -rf media/
rm -rf __pycache__/
rm -rf temp/

# 3. Reinstall
pip install -r requirements.txt

# 4. Set up fresh
python manage.py migrate
python manage.py setup_resume_system --create-superuser

# 5. Start server
python manage.py runserver
```

## 📚 Additional Resources

- **[Getting Started Guide](getting-started.md)** - Complete setup from zero
- **[User Manual](user-manual.md)** - How to use the system
- **[Developer Guide](developer-guide.md)** - Technical details
- **[API Documentation](api-documentation.md)** - API reference
- **[FAQ](faq.md)** - Frequently asked questions

---

**Remember**: Most problems have simple solutions. Don't panic - we're here to help! 🚀
