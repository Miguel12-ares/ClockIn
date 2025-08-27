from app import app


def test_admin_dashboard_access():
    with app.test_client() as client:
        response = client.get('/admin/dashboard', follow_redirects=False)
        assert response.status_code == 200


def test_admin_users_access():
    with app.test_client() as client:
        response = client.get('/admin/users', follow_redirects=False)
        assert response.status_code == 200


