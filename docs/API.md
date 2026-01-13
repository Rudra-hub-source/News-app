# News Management App API Documentation

## Endpoints

### Articles
- `GET /` - Homepage with latest articles
- `GET /articles` - List all articles
- `POST /articles/create` - Create new article
- `GET /articles/<id>` - View article details
- `POST /articles/edit/<id>` - Update article
- `POST /articles/delete/<id>` - Delete article
- `GET /articles/trending` - Get trending articles
- `GET /articles/latest` - Get latest articles

### Media
- `POST /articles/upload-image/<id>` - Upload image for article
- `POST /media/delete/<id>` - Delete media file

### Categories
- `GET /category/<name>` - Get articles by category

### Database
- `GET /initdb` - Initialize database with test data