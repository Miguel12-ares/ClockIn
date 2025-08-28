#!/usr/bin/env python3
"""
Script para probar el login y diagnosticar problemas
"""
import requests
import json

def test_login():
    """Probar el endpoint de login"""
    url = "http://localhost:5000/auth/login"
    
    # Datos de prueba
    data = {
        "idDocumento": "111",
        "password": "123456"
    }
    
    print("🔄 Probando login...")
    print(f"URL: {url}")
    print(f"Datos: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        
        print(f"\n📊 Respuesta:")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Login exitoso!")
            response_data = response.json()
            print(f"Respuesta JSON: {json.dumps(response_data, indent=2)}")
            
            # Probar el token
            if 'data' in response_data and 'access_token' in response_data['data']:
                token = response_data['data']['access_token']
                print(f"\n🔑 Token obtenido: {token[:50]}...")
                
                # Probar endpoint protegido
                test_protected_endpoint(token)
                
        else:
            print("❌ Login falló")
            try:
                error_data = response.json()
                print(f"Error JSON: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error Text: {response.text}")
                
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def test_protected_endpoint(token):
    """Probar un endpoint protegido con el token"""
    url = "http://localhost:5000/auth/me"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    print(f"\n🔄 Probando endpoint protegido...")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Endpoint protegido accesible!")
            response_data = response.json()
            print(f"Respuesta: {json.dumps(response_data, indent=2)}")
        else:
            print("❌ Endpoint protegido falló")
            try:
                error_data = response.json()
                print(f"Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error Text: {response.text}")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_login()
