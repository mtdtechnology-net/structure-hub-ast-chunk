from astchunk import ASTChunkBuilder

def test_dockerfile():
    """Test Dockerfile chunking"""
    print("\n=== Testing Dockerfile ===")
    
    dockerfile = """
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV PORT=8080

EXPOSE 8080

CMD ["python", "app.py"]
"""
    
    configs = {
        "max_chunk_size": 100,
        "language": "dockerfile",
        "metadata_template": "default"
    }
    
    chunk_builder = ASTChunkBuilder(**configs)
    chunks = chunk_builder.chunkify(dockerfile)
    
    print(f"✓ Generated {len(chunks)} chunks")
    assert len(chunks) > 0
    
    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i+1}: {len(chunk['content'])} chars")
    
    print("✓ Dockerfile test passed\n")


def test_package_json():
    """Test package.json chunking"""
    print("=== Testing package.json ===")
    
    package_json = """
{
  "name": "my-app",
  "version": "1.0.0",
  "description": "Sample application",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "test": "jest",
    "build": "webpack --mode production",
    "dev": "nodemon index.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "axios": "^1.4.0",
    "dotenv": "^16.0.3"
  },
  "devDependencies": {
    "jest": "^29.5.0",
    "nodemon": "^2.0.22",
    "webpack": "^5.88.0"
  },
  "engines": {
    "node": ">=16.0.0",
    "npm": ">=8.0.0"
  }
}
"""
    
    configs = {
        "max_chunk_size": 150,
        "language": "json",
        "metadata_template": "default"
    }
    
    chunk_builder = ASTChunkBuilder(**configs)
    chunks = chunk_builder.chunkify(package_json)
    
    print(f"✓ Generated {len(chunks)} chunks")
    assert len(chunks) > 0
    
    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i+1}: {len(chunk['content'])} chars")
    
    print("✓ package.json test passed\n")


def test_pom_xml():
    """Test pom.xml chunking"""
    print("=== Testing pom.xml ===")
    
    pom_xml = """
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    
    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>
    
    <properties>
        <java.version>17</java.version>
        <spring.version>3.1.0</spring.version>
    </properties>
    
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <version>${spring.version}</version>
        </dependency>
        
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
            <version>42.6.0</version>
        </dependency>
        
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <version>1.18.28</version>
            <scope>provided</scope>
        </dependency>
    </dependencies>
    
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
"""
    
    configs = {
        "max_chunk_size": 200,
        "language": "xml",
        "metadata_template": "default"
    }
    
    chunk_builder = ASTChunkBuilder(**configs)
    chunks = chunk_builder.chunkify(pom_xml)
    
    print(f"✓ Generated {len(chunks)} chunks")
    assert len(chunks) > 0
    
    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i+1}: {len(chunk['content'])} chars")
    
    print("✓ pom.xml test passed\n")


def test_pyproject_toml():
    """Test pyproject.toml chunking"""
    print("=== Testing pyproject.toml ===")
    
    pyproject_toml = """
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
version = "1.0.0"
description = "A sample Python package"
authors = [
    {name = "John Doe", email = "john@example.com"}
]
requires-python = ">=3.8"
dependencies = [
    "requests>=2.28.0",
    "pydantic>=2.0.0",
    "click>=8.1.0"
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "mypy>=1.0.0"
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"

[tool.black]
line-length = 100
target-version = ['py38', 'py39', 'py310']

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
"""
    
    configs = {
        "max_chunk_size": 150,
        "language": "toml",
        "metadata_template": "default"
    }
    
    chunk_builder = ASTChunkBuilder(**configs)
    chunks = chunk_builder.chunkify(pyproject_toml)
    
    print(f"✓ Generated {len(chunks)} chunks")
    assert len(chunks) > 0
    
    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i+1}: {len(chunk['content'])} chars")
    
    print("✓ pyproject.toml test passed\n")


def test_application_properties():
    """Test .properties file chunking"""
    print("=== Testing application.properties ===")
    
    properties_file = """
# Database Configuration
spring.datasource.url=jdbc:postgresql://localhost:5432/mydb
spring.datasource.username=dbuser
spring.datasource.password=dbpass
spring.datasource.driver-class-name=org.postgresql.Driver

# JPA Configuration
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.PostgreSQLDialect

# Server Configuration
server.port=8080
server.servlet.context-path=/api

# Logging Configuration
logging.level.root=INFO
logging.level.com.example=DEBUG
logging.pattern.console=%d{yyyy-MM-dd HH:mm:ss} - %msg%n

# Application Configuration
app.name=MyApplication
app.version=1.0.0
"""
    
    configs = {
        "max_chunk_size": 120,
        "language": "properties",
        "metadata_template": "default"
    }
    
    chunk_builder = ASTChunkBuilder(**configs)
    chunks = chunk_builder.chunkify(properties_file)
    
    print(f"✓ Generated {len(chunks)} chunks")
    assert len(chunks) > 0
    
    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i+1}: {len(chunk['content'])} chars")
    
    print("✓ application.properties test passed\n")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("CONFIG & BUILD FILES CHUNKING TEST SUITE")
    print("="*60)
    
    try:
        test_dockerfile()
        test_package_json()
        test_pom_xml()
        test_pyproject_toml()
        test_application_properties()
        
        print("="*60)
        print("✓✓✓ ALL CONFIG FILE TESTS PASSED ✓✓✓")
        print("="*60 + "\n")
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}\n")
        import traceback
        traceback.print_exc()
