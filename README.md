# Phidelis Ann Foundation - Django Website

A complete Django website for the Phidelis Ann Foundation, featuring a beautiful design with images, animations, and multiple pages.

## Features

- **Home Page**: Hero section with background image, animated statistics, mission cards, impact gallery
- **About Page**: Organization story, core values, team section, location information
- **Programs Page**: Detailed program descriptions with images
- **Gallery Page**: Filterable image gallery with lightbox functionality
- **Contact Page**: Contact form, donation options, volunteer signup

## Project Structure

```
phidelis_foundation/
├── phidelis_foundation/       # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── main/                       # Main application
│   ├── templates/main/        # HTML templates
│   │   ├── index.html         # Home page
│   │   ├── about.html         # About page
│   │   ├── programs.html      # Programs page
│   │   ├── gallery.html       # Gallery page
│   │   └── contact.html       # Contact page
│   ├── static/main/images/    # All images (12 total)
│   ├── views.py               # View functions
│   ├── urls.py                # URL patterns
│   └── models.py              # Database models
├── templates/
│   └── base.html              # Base template
├── manage.py
└── README.md
```

## Images Included (12 Total)

1. `hero_children_classroom.jpg` - Hero section background
2. `girl_child_education.jpg` - About section
3. `community_outreach.jpg` - Gallery/Impact
4. `children_studying_together.jpg` - Gallery/Impact
5. `uniform_distribution.jpg` - Programs/Outreach
6. `girls_mentorship.jpg` - Programs/Mentorship
7. `hygiene_education.jpg` - Programs/Health
8. `kakamega_village.jpg` - About/Location
9. `school_supplies.jpg` - Programs/Education
10. `teacher_portrait.jpg` - About/Team
11. `children_playing.jpg` - Gallery/Community
12. `volunteer_packing.jpg` - Gallery/Volunteer

## Installation

1. Install Django:
```bash
pip install django
```

2. Navigate to the project directory:
```bash
cd phidelis_foundation
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

6. Open your browser and visit:
```
http://127.0.0.1:8000/
```

## Customization

### Colors
The website uses a custom color palette defined in `base.html`:
- `--paf-green`: #1A3D2E (Primary dark green)
- `--paf-gold`: #C4A962 (Accent gold)
- `--paf-cream`: #F5F1E8 (Background cream)
- `--paf-beige`: #E8E0D0 (Secondary background)

### Adding More Images
1. Place new images in `main/static/main/images/`
2. Reference them in templates using: `{% static 'main/images/filename.jpg' %}`

### Modifying Content
- Edit text content in the respective template files
- Update statistics in `main/views.py`
- Add new pages by creating templates and adding URL patterns

## Deployment

For production deployment:

1. Set `DEBUG = False` in `settings.py`
2. Add your domain to `ALLOWED_HOSTS`
3. Collect static files:
```bash
python manage.py collectstatic
```
4. Use a production WSGI server like Gunicorn
5. Configure a web server like Nginx

## Credits

- Design: Phidelis Ann Foundation
- Images: AI-generated for demonstration purposes
- Icons: [Lucide Icons](https://lucide.dev/)
- Fonts: Google Fonts (Cormorant Garamond, Inter)
- CSS Framework: Tailwind CSS

## License

This project is created for Phidelis Ann Foundation. All rights reserved.
