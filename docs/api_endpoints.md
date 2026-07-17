# API Endpoints

## Media Manager API

### Search Files
```
GET /media/api/search/
```
**Query Parameters:**
- `q` (string, optional) — Search query (matches title, filename, alt_text)
- `type` (string, optional) — Filter by type: `IMAGE`, `VIDEO`, `DOCUMENT`, `AUDIO`, `OTHER`
- `folder` (uuid, optional) — Filter by folder UUID

**Response:**
```json
{
    "files": [
        {
            "id": "uuid",
            "title": "filename.jpg",
            "file_url": "/media/uploads/filename-abc123.jpg",
            "thumbnail_url": "/media/thumbnails/thumb_uuid.jpg",
            "file_type": "IMAGE",
            "formatted_size": "2.3 MB",
            "type_badge_color": "bg-green-100 text-green-800"
        }
    ]
}
```

**Authentication:** Required (Admin only)

---

## Settings API

All settings are managed via standard Django form POST requests to their respective URLs. No REST API endpoints — settings are singleton models managed through admin UI.

---

## Notes
- All API endpoints require admin authentication
- File upload is handled via multipart form POST to `/media/upload/`
- Bulk operations use standard form POST with `file_ids` array
