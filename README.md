# 🌐 DALI Social

A full-stack social media platform built for the DALI Lab community at Dartmouth College. Connect with fellow lab members, share updates, and discover the amazing personalities that make up our innovative team.

![DALI Social Banner](static/images/fav.png)

## ✨ Features

### 👥 Member Profiles
- Browse all DALI Lab members with rich profile information
- Filter members by role (Developer, Designer, PM, Core Team, Mentor)
- Search by name, major, minor, or hometown
- View detailed profiles with favorite things, quotes, and fun facts

### 📝 Posts & Feed
- Create and share posts with text, images, or links
- Like and comment on posts from fellow members
- Real-time feed of community updates
- Rich post interactions with engagement metrics

### 🤝 Connections
- Send and receive connection requests
- Build your professional network within DALI
- Track pending requests and accepted connections
- Discover suggested connections

### 🔌 REST API
- Full CRUD operations for members via API
- Search and filter endpoints for data visualization
- Pagination and ordering support
- Designed for frontend integration

## 🚀 Live Demo

**Deployed Application:** *Coming soon on Render*

## 📸 Screenshots

| Member Directory | Profile View | Feed |
|:---:|:---:|:---:|
| ![Members](https://via.placeholder.com/300x200?text=Member+List) | ![Profile](https://via.placeholder.com/300x200?text=Profile+View) | ![Feed](https://via.placeholder.com/300x200?text=Post+Feed) |

| Connections | API Endpoint | Mobile View |
|:---:|:---:|:---:|
| ![Connections](https://via.placeholder.com/300x200?text=Connections) | ![API](https://via.placeholder.com/300x200?text=REST+API) | ![Mobile](https://via.placeholder.com/300x200?text=Mobile+View) |

## 🛠️ Tech Stack

### Backend
- **Django 4.2** - High-level Python web framework
- **Django REST Framework** - Powerful API toolkit
- **SQLite** - Lightweight database (easily swappable to PostgreSQL)
- **Google OAuth2** - Secure authentication via social-auth-app-django

### Frontend
- **Django Templates** - Server-side rendering
- **Tailwind CSS** - Utility-first CSS framework (via CDN)
- **Font Awesome** - Icon library
- **DM Sans** - Clean, modern typography

### Deployment Ready
- **WhiteNoise** - Static file serving
- **Render** - Cloud hosting compatible
- **Docker** - Containerization ready

## 📋 Setup Instructions

### Prerequisites
- Python 3.10+
- pip (Python package manager)
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/gcl140/dali_social.git
   cd dali_social
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r req.txt
   ```

4. **Set up environment variables** (optional for Google OAuth)
   ```bash
   export GOOGLE_CLIENT_ID='your-google-client-id'
   export GOOGLE_CLIENT_SECRET='your-google-client-secret'
   export SECRET_KEY='your-secret-key'
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Load sample DALI member data** (if available)
   ```bash
   python manage.py loaddata members/fixtures/members.json
   ```
   
   Or import from the DALI social media JSON:
   ```bash
   python manage.py import_members
   ```

7. **Create a superuser** (for admin access)
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Main app: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/
   - API endpoints: http://127.0.0.1:8000/api/

## 🔗 API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/members/` | List all members (paginated) |
| `POST` | `/api/members/` | Create a new member |
| `GET` | `/api/members/{id}/` | Retrieve a specific member |
| `PUT` | `/api/members/{id}/` | Update a member |
| `DELETE` | `/api/members/{id}/` | Delete a member |

### Query Parameters
- `?search=` - Search by name, major, minor, or hometown
- `?ordering=name` - Order by field (name, year, created_at)
- `?page=` - Pagination

### Example Request
```bash
# Get all developers
curl http://127.0.0.1:8000/api/members/?search=developer

# Get member details
curl http://127.0.0.1:8000/api/members/1/
```

### Example Response
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

## 📖 Learning Journey

### What inspired this project?
The DALI Lab is more than just a workspace—it's a community of passionate innovators, designers, and developers. Walking into the lab, you're immediately struck by the diverse backgrounds and talents of its members. This platform was born from a desire to capture that energy digitally, making it easy for members to discover each other's stories, interests, and what makes each person unique beyond their technical skills.

The inspiration came from seeing how social connections at DALI often happen organically through shared projects or chance encounters. A digital space could amplify these connections, helping newer members discover potential collaborators and friends based on shared interests, hometowns, or favorite Dartmouth traditions.

### Potential Impact
- **For new members**: Quickly discover mentors and peers with similar interests
- **For project teams**: Find collaborators with complementary skills
- **For the broader community**: Document and celebrate the diverse backgrounds that make DALI special
- **For alumni**: Stay connected with the lab community beyond graduation

### New Technologies Learned

**Django REST Framework (DRF)**: Chose DRF for building the API because it provides powerful serialization, viewsets that reduce boilerplate code, and built-in support for pagination and filtering. The learning curve was worth it—DRF's browsable API made development and debugging significantly easier.

**Tailwind CSS**: Coming from traditional CSS, Tailwind's utility-first approach initially felt verbose. However, the rapid prototyping capabilities proved invaluable. Being able to style components directly in templates without context-switching to separate stylesheets accelerated the UI development significantly.

**Social Authentication (OAuth2)**: Implementing Google OAuth through `social-auth-app-django` taught me about authentication flows, token management, and the importance of secure session handling. The pipeline architecture for customizing user creation was particularly enlightening.

---

## 🔧 Technical Rationale

### Architecture Decisions

**Why Django over other frameworks?**
Django's "batteries included" philosophy was ideal for this project. The built-in admin interface, ORM, and authentication system allowed rapid development. For a community platform where content management is crucial, Django's admin alone saved significant development time. The project structure with separate apps (members, posts, connections) follows Django conventions and keeps concerns nicely separated.

**Why server-side rendering with API support?**
The hybrid approach—Django templates for the main UI with a REST API for data access—provides the best of both worlds. Server-side rendering offers excellent SEO and initial load performance, while the API enables future mobile apps or frontend frameworks to consume the same data.

**Database model design**
The Member model is intentionally separate from the CustomUser model. This allows DALI member data (imported from the JSON dataset) to exist independently of authentication users. When a user signs up, they can be linked to their existing Member profile. This separation also makes the API cleaner for data visualization projects that don't need authentication logic.

### Key Technical Tradeoffs

1. **SQLite vs PostgreSQL**: Chose SQLite for development simplicity and easy local setup. The codebase is designed for easy migration to PostgreSQL for production (just change DATABASES settings).

2. **Tailwind CDN vs Build Process**: Used the CDN for rapid development, accepting slightly larger page loads in exchange for simpler setup. For production, a proper Tailwind build would reduce the CSS payload.

3. **Session-based vs Token Authentication**: Chose session-based auth with OAuth for simplicity and browser compatibility. Token auth could be added for mobile API access without changing the core architecture.

### The Most Difficult Bug

**The Problem**: After implementing Google OAuth, users could log in but the system couldn't find their associated Member profile. The error occurred deep in the views when trying to access `request.user.name`.

**The Investigation**: The issue stemmed from the CustomUser model having a `name` field, but Member profiles being keyed on the `name` string. When users signed up via Google OAuth, their `name` field was populated from their Google profile, but no corresponding Member object existed.

**The Solution**: Implemented an auto-linking mechanism in the view layer:
```python
member, created = Member.objects.get_or_create(
    name=request.user.name,
    defaults={"year": "2024"}
)
```

This elegantly handles both cases—existing members with matching names get linked, and new users get a fresh Member profile created. The debugging process taught me about Django's authentication middleware and the importance of consistent data modeling across related models.

---

## 🤖 AI Usage

Yes, AI tools were used as collaborative partners during development.

### Example Prompt & Adaptation

**Prompt used:**
> "Create a Django view that allows users to update their member profile with form validation"

**AI's initial output:**
```python
def profile_update(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    form = MemberProfileForm(request.POST or None, instance=member)
    if form.is_valid():
        form.save()
        return redirect('member_detail', pk=member.pk)
    return render(request, 'members/profile_update.html', {'form': form})
```

**What I had to adapt:**

1. **Missing authentication**: Added `@login_required` decorator since profile editing should require authentication.

2. **No current user handling**: The AI assumed `member_id` would always be provided. I needed to handle the case where users edit their own profile without an ID in the URL:
   ```python
   if member_id:
       member = get_object_or_404(Member, id=member_id)
   else:
       member, created = Member.objects.get_or_create(
           name=request.user.name,
           defaults={"year": "2024"}
       )
   ```

3. **Missing user feedback**: Added Django messages for success/error feedback that the AI didn't include.

4. **Template context**: Added `is_editing: True` flag to help the template differentiate between view and edit modes.

This example illustrates how AI tools accelerate development by providing solid starting points, but real-world requirements—authentication, edge cases, UX considerations—require human judgment and project-specific knowledge to implement correctly.

---

## 📁 Project Structure

```
dali_social/
├── dali_social/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── members/              # Member profiles app
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── templates/
├── posts/                # Posts and feed app
│   ├── models.py
│   ├── views.py
│   └── templates/
├── connections/          # Connection requests app
│   ├── models.py
│   ├── views.py
│   └── templates/
├── yuzzaz/               # Custom user authentication
│   ├── models.py
│   └── views.py
├── templates/            # Base templates
│   └── base.html
├── static/               # Static assets
│   ├── css/
│   ├── js/
│   └── images/
├── manage.py
├── req.txt               # Python dependencies
└── README.md
```

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **DALI Lab** at Dartmouth College for the inspiration and member data
- The Django and Django REST Framework communities
- Tailwind CSS for the beautiful utility-first styling approach

---

<p align="center">
  Built with ❤️ for the DALI Lab community
</p>
