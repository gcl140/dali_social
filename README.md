# 🌐 DALI Social

A full-stack social platform built for the DALI Lab community at Dartmouth College. Connect with fellow lab members, share updates, and discover the amazing people behind the projects.

![DALI Social Banner](static/images/fav.png)

## ✨ What You Can Do

### 👥 Discover People
- Browse all DALI Lab members with rich profiles
- Filter by role (Developer, Designer, PM, Core Team, Mentor)
- Search by name, major, minor, or hometown
- Learn about members' favorite things, quotes, and fun facts

### 📝 Share & Connect
- Create posts with text, images, or links
- Like and comment on community updates
- See real-time activity in your feed
- Track engagement on your posts

### 🤝 Build Your Network
- Send and receive connection requests
- Grow your professional network within DALI
- Manage pending requests and connections
- Get suggestions for new connections

### 🔌 API Access
- Full CRUD operations for member data
- Search and filter endpoints
- Pagination and sorting support
- Ready for data visualization projects

## 🚀 See It Live

**Live Application:** *Live on PythonAnywhere: https://maghettoni.pythonanywhere.com/*

## 🛠️ Built With

### Backend
- **Django 4.2** - Python web framework
- **Django REST Framework** - API toolkit
- **SQLite** - Database (easy switch to PostgreSQL)
- **Google OAuth2** - Secure login, and email auth

### Frontend
- **Django Templates** - Server-side rendering
- **Tailwind CSS** - Styling via CDN
- **Font Awesome** - Icons
- **DM Sans** - Clean typography

### Deployment Ready
- **WhiteNoise** - Static files
- **PythonAnywhere** - Cloud hosting

## 🚦 Get Started

### What You'll Need
- Python 3.9+
- pip
- Git

### Local Setup

1. **Get the code**
   ```bash
   git clone https://github.com/gcl140/dali_social.git
   cd dali_social
   ```

2. **Set up your environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install packages**
   ```bash
   pip install -r req.txt
   ```

4. **Set up environment** (optional for Google login)
   ```bash
   export GOOGLE_CLIENT_ID='your-google-client-id'
   export GOOGLE_CLIENT_SECRET='your-google-client-secret'
   export SECRET_KEY='your-secret-key'
   ```

5. **Set up database**
   ```bash
   python manage.py migrate
   ```

6. **Add sample data** (if available)
   ```bash
   python manage.py import_dali_dict members.json
   ```
   

7. **Create admin account**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the server**
   ```bash
   python manage.py runserver
   ```

9. **Open your browser**
   - Main app: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/


### Search & Filter
- `?search=` - Search names, majors, minors, hometowns
- `?ordering=name` - Sort by field
- `?page=` - Pagination



### Sample Response
```json
{
    "id": 1,
    "name": "Alex Thompson",
    "year": "2025",
    "roles": ["Developer", "Designer"],
    "major": "Computer Science",
    "minor": "Digital Arts",
    "home": "San Francisco, CA",
    "quote": "Code is poetry",
    "picture": "https://example.com/photo.jpg",
    "created_at": "2024-01-15T10:30:00Z"
}
```

---

## 💡 The Story Behind This Project

### Why Build This?
The DALI Lab isn't just a workspace—it's a community of passionate creators. Every time I walk into the lab, I'm struck by the incredible diversity of backgrounds and talents. People come from different majors, hometowns, and interests, yet they all share this drive to build amazing things.

I wanted to capture that energy digitally. While we work together on projects, it's often hard to learn about each other beyond our technical roles. What are people's favorite books? Where did they grow up? What inspires them? This platform helps answer those questions and makes it easier for members to connect on a personal level.

### What I Hope It Achieves
- **For new members**: Quickly find mentors and peers who share your interests
- **For project teams**: Discover collaborators with complementary skills
- **For the community**: Celebrate the diverse backgrounds that make DALI special
- **For alumni**: Stay connected with the lab beyond graduation

### Technologies I Learned

**Django REST Framework**: I chose DRF for the API because it handles serialization beautifully and reduces repetitive code. The learning curve was steep at first, but the browsable API feature made debugging so much easier once I got the hang of it.

**Tailwind CSS**: Coming from traditional CSS, Tailwind's utility classes felt strange initially. But once I started building, I loved how quickly I could prototype interfaces without constantly switching between files.

**OAuth2 Authentication**: Implementing Google login taught me about authentication flows and secure session management. The pipeline system for customizing user creation was particularly interesting to work with.

---

## 🔧 Technical Choices

### Why Django?
Django's "batteries included" approach was perfect for this project. The built-in admin interface alone saved me countless hours. Having separate apps for members, posts, and connections kept everything organized and made the codebase easy to navigate.

### Hybrid Approach
I went with server-side rendering for the main UI but added a REST API for data access. This gives us fast initial page loads while still allowing for future mobile apps or different frontends to use the same backend.

### Member vs User Models
I kept Member profiles separate from authentication users. This means we can import all the existing DALI member data without worrying about login systems. When someone signs up, we just link them to their existing profile.

### Tradeoffs Made

1. **SQLite for Now**: Using SQLite for development simplicity, but the code is ready to switch to PostgreSQL for production.

2. **Tailwind via CDN**: Faster development setup, though a proper build process would be better for production CSS size.

3. **Session Authentication**: Chose session-based auth for browser compatibility. Could add token auth later for mobile apps.

### The Trickiest Bug

**The Problem**: After getting Google OAuth working, users could log in but the system couldn't find their Member profiles. The error happened deep in the views when trying to access user details.

**What Was Happening**: The issue was that the CustomUser model had a `name` field, but Member profiles were separate. When people signed up via Google, their user account was created but no corresponding Member profile existed.

**The Fix**: I added automatic profile linking:
```python
member, created = Member.objects.get_or_create(
    name=request.user.name,
    defaults={"year": "2024"}
)
```

Now when users sign in, the system either finds their existing Member profile or creates a new one. Debugging this taught me a lot about how Django's authentication system works and the importance of keeping related data models in sync.

---

## 🤖 Working with AI

Yes, I used AI tools as coding partners during development. They were great for getting started quickly, but always required human judgment to get right.

### Example Collaboration

**What I asked:**
> "Create a Django view for updating member profiles with form validation"

**What AI suggested:**
```python
def profile_update(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    form = MemberProfileForm(request.POST or None, instance=member)
    if form.is_valid():
        form.save()
        return redirect('member_detail', pk=member.pk)
    return render(request, 'members/profile_update.html', {'form': form})
```

**What I had to add:**

1. **Authentication**: Added `@login_required` since you should only edit your own profile

2. **User handling**: The AI assumed we'd always have a member_id, but I needed to handle cases where users edit their own profiles without an ID

3. **User experience**: Added success/error messages that the AI didn't include

4. **Template logic**: Added flags to help templates know when we're in edit mode vs view mode

This pattern repeated throughout the project—AI gave me solid starting points, but real-world considerations like security, edge cases, and user experience needed human thinking.

---

## 📁 Project Layout

```
dali_social/
├── dali_social/          # Project settings
├── members/              # Member profiles
├── posts/                # Posts and feed
├── connections/          # Connection system
├── yuzzaz/               # User authentication
├── templates/            # Base templates
├── static/               # CSS, JS, images
├── manage.py
├── req.txt              # Dependencies
└── README.md
```

## 🤝 Want to Contribute?

I'd love your help! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/cool-improvement`)
3. Commit your changes (`git commit -m 'Add cool improvement'`)
4. Push to the branch (`git push origin feature/cool-improvement`)
5. Open a Pull Request

## 📄 License

MIT License - feel free to use this code for your own projects!

## 🙏 Thanks

- **DALI Lab** for the inspiration and community
- **Django** and **Tailwind** communities for amazing tools
- Everyone who tested early versions and gave feedback

---

<p align="center">
  Made with ❤️ for the DALI Lab community
</p>