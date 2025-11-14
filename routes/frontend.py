"""
Frontend routes to serve HTML templates.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from pathlib import Path

router = APIRouter()

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"


@router.get("/", response_class=HTMLResponse)
async def index():
    """Serve the main index page."""
    index_file = TEMPLATES_DIR / "index.html"
    if not index_file.exists():
        return "<h1>Face Recognition System</h1><p>Templates not found</p>"
    
    # Simple HTML serving - strip Django template tags for now
    content = index_file.read_text()
    # Remove Django template tags for basic testing
    content = content.replace("{% extends 'base.html' %}", "")
    content = content.replace("{% block title %}Face Recognition{% endblock %}", "")
    content = content.replace("{% block extra_head %}", "")
    content = content.replace("{% endblock %}", "")
    content = content.replace("{% block content %}", "")
    content = content.replace("{% block extra_scripts %}", "")
    content = content.replace("{% csrf_token %}", "")
    content = content.replace("{% url 'face_list' %}", "/api/faces/")
    # Fix detect endpoint
    content = content.replace('"/detect/"', '"/api/faces/detect"')
    
    # Wrap in basic HTML structure
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Face Recognition</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
    {content}
</body>
</html>"""


@router.get("/login", response_class=HTMLResponse)
async def login():
    """Serve the login page."""
    return """<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
    <div class="container mx-auto px-4 py-16 max-w-md">
        <div class="max-w-md w-full space-y-8 p-8 bg-white rounded-lg shadow-lg">
            <div class="text-center">
                <h1 class="text-2xl font-bold text-blue-600">Face Recognition System</h1>
                <p class="mt-2 text-gray-600">Sign in to your account</p>
            </div>
            <form class="mt-8 space-y-6" method="POST">
                <div class="rounded-md shadow-sm space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Username</label>
                        <input type="text" name="username" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Password</label>
                        <input type="password" name="password" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                    </div>
                </div>
                <button type="submit" class="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700">
                    Sign in
                </button>
            </form>
            <div class="text-center mt-4">
                <p class="text-sm text-gray-600">
                    Don't have an account? <a href="/register" class="font-medium text-blue-600 hover:text-blue-500">Create one</a>
                </p>
            </div>
        </div>
    </div>
</body>
</html>"""




@router.get("/faces/add", response_class=HTMLResponse)
async def add_face():
    """Serve the add face page."""
    return """<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100">
    <div class="container mx-auto px-4 py-8 max-w-2xl">
        <div class="bg-white rounded-lg shadow-lg p-8">
            <h1 class="text-3xl font-bold text-blue-600 mb-6">Register New Face</h1>
            <form id="faceForm" class="space-y-6">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Name</label>
                    <input type="text" id="name" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" required>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Access Permission</label>
                    <select id="is_allowed" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
                        <option value="true">✅ Allowed</option>
                        <option value="false">⛔ Denied</option>
                    </select>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Face Photo</label>
                    <input type="file" id="image" accept="image/*" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" required>
                </div>
                <button type="submit" class="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 font-medium">Register Face</button>
            </form>
            <div id="result" class="mt-4 hidden"></div>
            <div class="mt-6 text-center">
                <a href="/" class="text-blue-600 hover:text-blue-700">← Back to Face Detection</a>
            </div>
        </div>
    </div>
    <script>
        document.getElementById('faceForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData();
            formData.append('name', document.getElementById('name').value);
            formData.append('is_allowed', document.getElementById('is_allowed').value === 'true');
            formData.append('image', document.getElementById('image').files[0]);
            
            try {
                const response = await fetch('/api/faces/', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                const resultDiv = document.getElementById('result');
                resultDiv.classList.remove('hidden');
                if (response.ok) {
                    resultDiv.className = 'mt-4 p-4 bg-green-100 text-green-700 rounded-lg';
                    resultDiv.textContent = '✓ Face registered successfully! ID: ' + data.id;
                    document.getElementById('faceForm').reset();
                } else {
                    resultDiv.className = 'mt-4 p-4 bg-red-100 text-red-700 rounded-lg';
                    resultDiv.textContent = '✗ Error: ' + (data.detail || 'Unknown error');
                }
            } catch (error) {
                const resultDiv = document.getElementById('result');
                resultDiv.classList.remove('hidden');
                resultDiv.className = 'mt-4 p-4 bg-red-100 text-red-700 rounded-lg';
                resultDiv.textContent = '✗ Error: ' + error.message;
            }
        });
    </script>
</body>
</html>"""


@router.get("/admin", response_class=HTMLResponse)
async def admin_dashboard():
    """Admin dashboard."""
    return """<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100">
    <div class="container mx-auto px-4 py-8">
        <div class="mb-8">
            <h1 class="text-4xl font-bold text-blue-600 mb-2">Admin Dashboard</h1>
            <p class="text-gray-600">Face Recognition System</p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div class="bg-white rounded-lg shadow p-6">
                <h3 class="text-gray-500 text-sm font-medium mb-2">Registered Faces</h3>
                <p id="totalFaces" class="text-3xl font-bold text-blue-600">-</p>
            </div>
            <div class="bg-white rounded-lg shadow p-6">
                <h3 class="text-gray-500 text-sm font-medium mb-2">Total Visits</h3>
                <p id="totalVisits" class="text-3xl font-bold text-green-600">-</p>
            </div>
            <div class="bg-white rounded-lg shadow p-6">
                <h3 class="text-gray-500 text-sm font-medium mb-2">Unknown Visitors</h3>
                <p id="unknownVisits" class="text-3xl font-bold text-red-600">-</p>
            </div>
        </div>
        
        <div class="flex gap-4 mb-6">
            <a href="/faces/add" class="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 font-medium">➕ Add New Face</a>
            <a href="/" class="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 font-medium">📸 Face Detection</a>
        </div>
        
        <div class="bg-white rounded-lg shadow mb-8">
            <div class="px-6 py-4 border-b">
                <h2 class="text-xl font-bold text-gray-800">Recent Visits</h2>
            </div>
            <div class="overflow-x-auto">
                <table class="w-full">
                    <thead class="bg-gray-50">
                        <tr>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Time</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Confidence</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Access</th>
                        </tr>
                    </thead>
                    <tbody id="visitsTable" class="divide-y divide-gray-200">
                        <tr><td colspan="4" class="px-6 py-4 text-center text-gray-500">Loading...</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
        
        <div class="bg-white rounded-lg shadow">
            <div class="px-6 py-4 border-b">
                <h2 class="text-xl font-bold text-gray-800">Registered Faces</h2>
            </div>
            <div id="facesList" class="p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <p class="text-gray-500">Loading...</p>
            </div>
        </div>
    </div>
    
    <script>
        async function loadData() {
            try {
                // Load faces
                const facesRes = await fetch('/api/faces/');
                const facesData = await facesRes.json();
                document.getElementById('totalFaces').textContent = facesData.total || 0;
                
                // Load visits
                const visitsRes = await fetch('/api/visits/');
                const visitsData = await visitsRes.json();
                document.getElementById('totalVisits').textContent = visitsData.total || 0;
                document.getElementById('unknownVisits').textContent = visitsData.unknown_count || 0;
                
                // Display visits
                const visitsTable = document.getElementById('visitsTable');
                if (visitsData.visits && visitsData.visits.length > 0) {
                    visitsTable.innerHTML = visitsData.visits.map(visit => `
                        <tr class="hover:bg-gray-50">
                            <td class="px-6 py-4 text-sm text-gray-900">${new Date(visit.timestamp).toLocaleString()}</td>
                            <td class="px-6 py-4 text-sm font-medium text-gray-900">${visit.person_name}</td>
                            <td class="px-6 py-4 text-sm text-gray-500">${visit.confidence}</td>
                            <td class="px-6 py-4 text-sm">
                                <span class="px-2 py-1 text-xs font-bold rounded-full ${visit.is_allowed ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}">
                                    ${visit.is_allowed ? '✓ ALLOWED' : '✗ DENIED'}
                                </span>
                            </td>
                        </tr>
                    `).join('');
                } else {
                    visitsTable.innerHTML = '<tr><td colspan="4" class="px-6 py-4 text-center text-gray-500">No visits yet</td></tr>';
                }
                
                // Display faces
                const facesList = document.getElementById('facesList');
                if (facesData.faces && facesData.faces.length > 0) {
                    facesList.innerHTML = facesData.faces.map(face => `
                        <div class="bg-gray-50 rounded-lg p-4 border ${face.is_allowed ? 'border-green-200' : 'border-red-200'}">
                            <div class="flex items-center gap-3 mb-2">
                                <div class="h-12 w-12 rounded-full bg-blue-100 flex items-center justify-center">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                    </svg>
                                </div>
                                <div>
                                    <h4 class="font-medium text-gray-900">${face.name}</h4>
                                    <p class="text-xs text-gray-500">ID: ${face.id}</p>
                                </div>
                            </div>
                            <span class="px-2 py-1 text-xs font-bold rounded-full ${face.is_allowed ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}">
                                ${face.is_allowed ? '✓ ALLOWED' : '✗ DENIED'}
                            </span>
                        </div>
                    `).join('');
                } else {
                    facesList.innerHTML = '<p class="text-gray-500">No faces registered yet</p>';
                }
            } catch (error) {
                console.error('Error loading data:', error);
            }
        }
        
        loadData();
        setInterval(loadData, 5000); // Refresh every 5 seconds
    </script>
</body>
</html>"""


@router.get("/register", response_class=HTMLResponse)
async def register():
    """Serve the registration page."""
    return """<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
    <div class="container mx-auto px-4 py-16 max-w-md">
        <div class="max-w-md w-full space-y-8 p-8 bg-white rounded-lg shadow-lg">
            <div class="text-center">
                <h1 class="text-2xl font-bold text-blue-600">Face Recognition System</h1>
                <p class="mt-2 text-gray-600">Create a new account</p>
            </div>
            <form class="mt-8 space-y-6" method="POST">
                <div class="rounded-md shadow-sm space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Username</label>
                        <input type="text" name="username" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Email</label>
                        <input type="email" name="email" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Password</label>
                        <input type="password" name="password" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Confirm Password</label>
                        <input type="password" name="password2" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                    </div>
                </div>
                <button type="submit" class="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700">
                    Create Account
                </button>
            </form>
            <div class="text-center mt-4">
                <p class="text-sm text-gray-600">
                    Already have an account? <a href="/login" class="font-medium text-blue-600 hover:text-blue-500">Sign in</a>
                </p>
            </div>
        </div>
    </div>
</body>
</html>"""
