# tests/test_yaml.py

from astchunk import ASTChunkBuilder

def test_openapi_specification():
    """Test chunking of OpenAPI 3.0 specification"""
    print("\n=== Testing OpenAPI Specification ===")
    
    openapi_yaml = """
openapi: 3.0.0
info:
  title: User Management API
  version: 1.0.0
  description: API for managing users and their profiles
  contact:
    email: api@example.com
servers:
  - url: https://api.example.com/v1
    description: Production server
  - url: https://staging-api.example.com/v1
    description: Staging server
paths:
  /users:
    get:
      summary: List all users
      operationId: listUsers
      tags:
        - users
      parameters:
        - name: limit
          in: query
          description: Maximum number of users to return
          required: false
          schema:
            type: integer
            format: int32
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
        '400':
          description: Bad request
    post:
      summary: Create a new user
      operationId: createUser
      tags:
        - users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/User'
      responses:
        '201':
          description: User created successfully
        '400':
          description: Invalid input
  /users/{userId}:
    get:
      summary: Get user by ID
      operationId: getUserById
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Successful response
        '404':
          description: User not found
components:
  schemas:
    User:
      type: object
      required:
        - id
        - email
      properties:
        id:
          type: string
        email:
          type: string
          format: email
        firstName:
          type: string
        lastName:
          type: string
"""
    
    configs = {
        "max_chunk_size": 200,
        "language": "yaml",
        "metadata_template": "default"
    }
    
    chunk_builder = ASTChunkBuilder(**configs)
    chunks = chunk_builder.chunkify(openapi_yaml)
    
    print(f"✓ Generated {len(chunks)} chunks")
    assert len(chunks) > 0
    
    # Verify content is preserved
    full_content = ''.join([c['content'] for c in chunks])
    assert 'openapi' in full_content.lower()
    assert 'paths' in full_content
    assert 'components' in full_content
    
    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i+1}: {len(chunk['content'])} chars")
        assert 'content' in chunk
        assert 'metadata' in chunk
    
    print("✓ OpenAPI test passed\n")


def test_docker_compose():
    """Test chunking of Docker Compose configuration"""
    print("=== Testing Docker Compose File ===")
    
    docker_compose = """
version: '3.8'
services:
  webapp:
    image: nginx:latest
    container_name: my_webapp
    ports:
      - "80:80"
      - "443:443"
    environment:
      - NODE_ENV=production
      - API_KEY=secret_key_value
      - DATABASE_URL=postgres://db:5432/myapp
    volumes:
      - ./app:/usr/share/nginx/html
      - ./config:/etc/nginx/conf.d
      - ./logs:/var/log/nginx
    depends_on:
      - db
      - redis
    networks:
      - app-network
    restart: always
  
  db:
    image: postgres:14-alpine
    container_name: postgres_db
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: dbuser
      POSTGRES_PASSWORD: dbpass
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    networks:
      - app-network
    restart: unless-stopped
  
  redis:
    image: redis:7-alpine
    container_name: redis_cache
    command: redis-server --appendonly yes
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - app-network
    restart: always

networks:
  app-network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
"""
    
    configs = {
        "max_chunk_size": 150,
        "language": "yaml",
        "metadata_template": "default"
    }
    
    chunk_builder = ASTChunkBuilder(**configs)
    chunks = chunk_builder.chunkify(docker_compose)
    
    print(f"✓ Generated {len(chunks)} chunks")
    assert len(chunks) > 0
    
    # Verify services are present
    full_content = ''.join([c['content'] for c in chunks])
    assert 'services' in full_content
    assert 'webapp' in full_content or 'db' in full_content
    
    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i+1}: {len(chunk['content'])} chars")
    
    print("✓ Docker Compose test passed\n")


def test_kubernetes_config():
    """Test chunking of Kubernetes configuration"""
    print("=== Testing Kubernetes Configuration ===")
    
    k8s_yaml = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
    environment: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80
        resources:
          limits:
            memory: "256Mi"
            cpu: "500m"
          requests:
            memory: "128Mi"
            cpu: "250m"
        env:
        - name: ENV_VAR_1
          value: "value1"
        - name: ENV_VAR_2
          valueFrom:
            secretKeyRef:
              name: my-secret
              key: password
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: LoadBalancer
"""
    
    configs = {
        "max_chunk_size": 180,
        "language": "yaml",
        "metadata_template": "default"
    }
    
    chunk_builder = ASTChunkBuilder(**configs)
    chunks = chunk_builder.chunkify(k8s_yaml)
    
    print(f"✓ Generated {len(chunks)} chunks")
    assert len(chunks) > 0
    
    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i+1}: {len(chunk['content'])} chars")
    
    print("✓ Kubernetes config test passed\n")


def test_ci_cd_pipeline():
    """Test chunking of CI/CD pipeline configuration (GitHub Actions)"""
    print("=== Testing CI/CD Pipeline (GitHub Actions) ===")
    
    github_actions = """
name: CI/CD Pipeline
on:
  push:
    branches:
      - main
      - develop
  pull_request:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11']
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: |
          pytest tests/ -v --cov=src --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
  
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: |
          docker build -t myapp:${{ github.sha }} .
      
      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker push myapp:${{ github.sha }}
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to production
        run: |
          echo "Deploying to production..."
"""
    
    configs = {
        "max_chunk_size": 200,
        "language": "yaml",
        "metadata_template": "default"
    }
    
    chunk_builder = ASTChunkBuilder(**configs)
    chunks = chunk_builder.chunkify(github_actions)
    
    print(f"✓ Generated {len(chunks)} chunks")
    assert len(chunks) > 0
    
    full_content = ''.join([c['content'] for c in chunks])
    assert 'jobs' in full_content
    
    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i+1}: {len(chunk['content'])} chars")
    
    print("✓ CI/CD pipeline test passed\n")


def test_application_config():
    """Test chunking of application configuration file"""
    print("=== Testing Application Configuration ===")
    
    app_config = """
# Application Configuration
app:
  name: MyApplication
  version: 2.1.0
  debug: false
  timezone: UTC

server:
  host: 0.0.0.0
  port: 8080
  workers: 4
  timeout: 30
  keepalive: 75

database:
  primary:
    host: db-primary.example.com
    port: 5432
    name: production_db
    username: db_user
    password: ${DB_PASSWORD}
    pool_size: 20
    max_overflow: 10
    ssl_mode: require
  
  replica:
    host: db-replica.example.com
    port: 5432
    name: production_db
    username: db_user
    password: ${DB_PASSWORD}
    pool_size: 10

cache:
  backend: redis
  host: redis.example.com
  port: 6379
  db: 0
  ttl: 3600
  max_connections: 50

logging:
  level: INFO
  format: json
  outputs:
    - type: console
      level: WARNING
    - type: file
      level: DEBUG
      path: /var/log/app/app.log
      max_size: 100MB
      backup_count: 5
    - type: syslog
      level: ERROR
      host: syslog.example.com
      port: 514

features:
  authentication: true
  registration: true
  email_verification: true
  two_factor_auth: false
  rate_limiting: true
  api_versioning: true

integrations:
  stripe:
    api_key: ${STRIPE_API_KEY}
    webhook_secret: ${STRIPE_WEBHOOK_SECRET}
  
  sendgrid:
    api_key: ${SENDGRID_API_KEY}
    from_email: noreply@example.com
  
  aws:
    region: us-east-1
    access_key: ${AWS_ACCESS_KEY}
    secret_key: ${AWS_SECRET_KEY}
    s3_bucket: my-app-uploads
"""
    
    configs = {
        "max_chunk_size": 150,
        "language": "yaml",
        "metadata_template": "default"
    }
    
    chunk_builder = ASTChunkBuilder(**configs)
    chunks = chunk_builder.chunkify(app_config)
    
    print(f"✓ Generated {len(chunks)} chunks")
    assert len(chunks) > 0
    
    full_content = ''.join([c['content'] for c in chunks])
    assert 'database' in full_content
    assert 'server' in full_content
    
    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i+1}: {len(chunk['content'])} chars")
    
    print("✓ Application config test passed\n")


def test_ansible_playbook():
    """Test chunking of Ansible playbook"""
    print("=== Testing Ansible Playbook ===")
    
    ansible_yaml = """
---
- name: Deploy web application
  hosts: webservers
  become: yes
  vars:
    app_name: myapp
    app_version: 1.0.0
    deploy_user: deployer
  
  tasks:
    - name: Update apt cache
      apt:
        update_cache: yes
        cache_valid_time: 3600
    
    - name: Install required packages
      apt:
        name:
          - nginx
          - python3
          - python3-pip
          - git
        state: present
    
    - name: Create application directory
      file:
        path: "/opt/{{ app_name }}"
        state: directory
        owner: "{{ deploy_user }}"
        group: "{{ deploy_user }}"
        mode: '0755'
    
    - name: Clone application repository
      git:
        repo: https://github.com/example/myapp.git
        dest: "/opt/{{ app_name }}"
        version: "v{{ app_version }}"
      become_user: "{{ deploy_user }}"
    
    - name: Install Python dependencies
      pip:
        requirements: "/opt/{{ app_name }}/requirements.txt"
        virtualenv: "/opt/{{ app_name }}/venv"
      become_user: "{{ deploy_user }}"
    
    - name: Configure nginx
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/sites-available/{{ app_name }}
      notify: Restart nginx
    
    - name: Enable site
      file:
        src: /etc/nginx/sites-available/{{ app_name }}
        dest: /etc/nginx/sites-enabled/{{ app_name }}
        state: link
      notify: Restart nginx
  
  handlers:
    - name: Restart nginx
      service:
        name: nginx
        state: restarted
"""
    
    configs = {
        "max_chunk_size": 180,
        "language": "yaml",
        "metadata_template": "default"
    }
    
    chunk_builder = ASTChunkBuilder(**configs)
    chunks = chunk_builder.chunkify(ansible_yaml)
    
    print(f"✓ Generated {len(chunks)} chunks")
    assert len(chunks) > 0
    
    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i+1}: {len(chunk['content'])} chars")
    
    print("✓ Ansible playbook test passed\n")


def test_small_config():
    """Test chunking of small configuration file"""
    print("=== Testing Small Config File ===")
    
    small_yaml = """
timeout: 30
retries: 3
debug: true
"""
    
    configs = {
        "max_chunk_size": 150,
        "language": "yaml",
        "metadata_template": "default"
    }
    
    chunk_builder = ASTChunkBuilder(**configs)
    chunks = chunk_builder.chunkify(small_yaml)
    
    print(f"✓ Generated {len(chunks)} chunks")
    assert len(chunks) > 0
    
    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i+1}: {len(chunk['content'])} chars")
    
    print("✓ Small config test passed\n")


def test_edge_cases():
    """Test edge cases"""
    print("=== Testing Edge Cases ===")
    
    # Empty YAML
    print("  Testing empty YAML...")
    configs = {
        "max_chunk_size": 150,
        "language": "yaml",
        "metadata_template": "default"
    }
    chunk_builder = ASTChunkBuilder(**configs)
    chunks = chunk_builder.chunkify("")
    print(f"    Empty YAML: {len(chunks)} chunks")
    
    # YAML with comments
    print("  Testing YAML with comments...")
    yaml_with_comments = """
# Main configuration
database:
  host: localhost  # development host
  port: 5432       # default postgres port
"""
    chunks = chunk_builder.chunkify(yaml_with_comments)
    print(f"    With comments: {len(chunks)} chunks")
    assert len(chunks) > 0
    
    # Multiline strings
    print("  Testing multiline strings...")
    yaml_multiline = """
description: |
  This is a long description
  that spans multiple lines
  and should be kept together
key: value
"""
    chunks = chunk_builder.chunkify(yaml_multiline)
    print(f"    Multiline: {len(chunks)} chunks")
    assert len(chunks) > 0
    
    print("✓ Edge cases test passed\n")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("YAML CHUNKING TEST SUITE")
    print("="*60)
    
    try:
        test_openapi_specification()
        test_docker_compose()
        test_kubernetes_config()
        test_ci_cd_pipeline()
        test_application_config()
        test_ansible_playbook()
        test_small_config()
        test_edge_cases()
        
        print("="*60)
        print("✓✓✓ ALL TESTS PASSED ✓✓✓")
        print("="*60 + "\n")
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}\n")
        import traceback
        traceback.print_exc()
