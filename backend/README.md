# Backend API – S2O Platform

This backend is the core API of the S2O-Platform, designed as a **multi-tenant SaaS system**
using **Flask Clean Architecture**.

## Responsibilities

- Provide REST APIs for Web and Mobile applications
- Handle authentication & authorization (JWT, RBAC)
- Support multi-tenant data isolation
- Manage restaurants, menus, orders, payments, and reviews
- Integrate AI modules (Chatbot QA & Recommendation Engine)

## Architecture

- Language: Python
- Framework: Flask
- Architecture: Clean Architecture (Domain – Service – Infrastructure – API)
- Database: PostgreSQL
- Cache & Realtime: Redis

> Source code will be implemented incrementally following Clean Architecture principles.

```bash
    ├── migrations
    ├── scripts
    │   └── run_postgres.sh
    ├── src
    │   ├── api
    │   │   ├── controllers
    │   │   │   └── ...  # controllers for the api
    │   │   ├── schemas
    │   │   │   └── ...  # Marshmallow schemas
    │   │   ├── middleware.py
    │   │   ├── responses.py
    │   │   └── requests.py
    │   ├── infrastructure
    │   │   ├── services
    │   │   │   └── ...  # Services that use third party libraries or services (e.g. email service)
    │   │   ├── databases
    │   │   │   └── ...  # Database adapaters and initialization
    │   │   ├── repositories
    │   │   │   └── ...  # Repositories for interacting with the databases
    │   │   └── models
    │   │   │   └── ...  # Database models
    │   ├── domain
    │   │   ├── constants.py
    │   │   ├── exceptions.py
    │   │   ├── models
    │   │   │   └── ...  # Business logic models
    │   ├── services
    │   │    └── ...  # Services for interacting with the domain (business logic)
    │   ├── app.py
    │   ├── config.py
    │   ├── cors.py
    │   ├── create_app.py
    │   ├── dependency_container.py
    │   ├── error_handler.py
    │   └── logging.py
```

## Domain Layer

## Services Layer

## Infrastructure Layer

## Download source code (CMD)
    git clone https://github.com/tudptse17520/S2O-Platform.git
## Kiểm tra đã cài python đã cài đặt trên máy chưa
    python --version
## Run app(backend)

    - Bước 1: Tạo môi trường ảo co Python (phiên bản 3.x)
        cd <root_project>
     ## Windows:
     		py -m venv .venv
     ## Unix/MacOS:
     		python3 -m venv .venv
    - Bước 2: Kích hoạt môi trường:
     ## Windows:
     		.venv\Scripts\activate.ps1
     ### Nếu xảy ra lỗi active .venv trên winos run powershell -->Administrator
         Set-ExecutionPolicy RemoteSigned -Force
     ## Unix/MacOS:
     		source .venv/bin/activate
     
    - Bước 3: Cài đặt các thư viện cần thiết
        cd backend/
     ## Install:
     		pip install -r requirements.txt
    - Bước 4: Chạy mã xử lý dữ liệu
     ## Run:
    		python app.py


     Truy câp http://127.0.0.1:5000
     Truy câp http://192.168.1.15:5000



## Create file .env in folder backend/.env
    
    FLASK_ENV=development
    SECRET_KEY=s2o-secret-key
