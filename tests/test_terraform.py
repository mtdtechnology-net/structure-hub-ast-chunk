import unittest
import tree_sitter as ts
from astchunk.astchunk_builder import ASTChunkBuilder


class TestHCLTerraformSupport(unittest.TestCase):
    """Test cases for HCL and Terraform file parsing support"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.max_chunk_size = 1000
        self.metadata_template = "default"
        
        # Sample Terraform/HCL code
        self.sample_terraform_code = '''
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  
  tags = {
    Name = "WebServer"
    Environment = "Production"
  }
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.web.id
}
'''
        
        self.sample_hcl_code = '''
locals {
  true = "true"
  false = "false"
}

service {
  name = "web"
  port = 8080
  
  check {
    interval = "10s"
    timeout  = "2s"
  }
}
'''

    def test_hcl_language_initialization(self):
        """Test that ASTChunkBuilder initializes correctly with 'hcl' language"""
        builder = ASTChunkBuilder(
            max_chunk_size=self.max_chunk_size,
            language="hcl",
            metadata_template=self.metadata_template
        )
        
        self.assertIsNotNone(builder.parser)
        self.assertEqual(builder.language, "hcl")
        
    def test_terraform_language_initialization(self):
        """Test that ASTChunkBuilder initializes correctly with 'terraform' language"""
        builder = ASTChunkBuilder(
            max_chunk_size=self.max_chunk_size,
            language="terraform",
            metadata_template=self.metadata_template
        )
        
        self.assertIsNotNone(builder.parser)
        self.assertEqual(builder.language, "terraform")
    
    def test_parse_terraform_resource_block(self):
        """Test parsing a Terraform resource block"""
        builder = ASTChunkBuilder(
            max_chunk_size=self.max_chunk_size,
            language="terraform",
            metadata_template=self.metadata_template
        )
        
        tree = builder.parser.parse(bytes(self.sample_terraform_code, "utf8"))
        root_node = tree.root_node
        
        # Verify parsing was successful (no errors)
        self.assertFalse(root_node.has_error)
        
        # Verify we can traverse the tree
        self.assertGreater(root_node.child_count, 0)
        
    def test_parse_hcl_file(self):
        """Test parsing a generic HCL file"""
        builder = ASTChunkBuilder(
            max_chunk_size=self.max_chunk_size,
            language="hcl",
            metadata_template=self.metadata_template
        )
        
        tree = builder.parser.parse(bytes(self.sample_hcl_code, "utf8"))
        root_node = tree.root_node
        
        # Verify parsing was successful
        self.assertFalse(root_node.has_error)
        self.assertGreater(root_node.child_count, 0)
    
    def test_terraform_variable_block_parsing(self):
        """Test parsing Terraform variable declarations"""
        variable_code = '''
variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}
'''
        builder = ASTChunkBuilder(
            max_chunk_size=self.max_chunk_size,
            language="terraform",
            metadata_template=self.metadata_template
        )
        
        tree = builder.parser.parse(bytes(variable_code, "utf8"))
        root_node = tree.root_node
        
        self.assertFalse(root_node.has_error)
        
    def test_terraform_output_block_parsing(self):
        """Test parsing Terraform output blocks"""
        output_code = '''
output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.web.id
}
'''
        builder = ASTChunkBuilder(
            max_chunk_size=self.max_chunk_size,
            language="terraform",
            metadata_template=self.metadata_template
        )
        
        tree = builder.parser.parse(bytes(output_code, "utf8"))
        root_node = tree.root_node
        
        self.assertFalse(root_node.has_error)
        
    def test_hcl_locals_block_parsing(self):
        """Test parsing HCL locals block"""
        locals_code = '''
locals {
  environment = "production"
  region      = "us-west-2"
  common_tags = {
    Project = "MyProject"
    Owner   = "DevOps"
  }
}
'''
        builder = ASTChunkBuilder(
            max_chunk_size=self.max_chunk_size,
            language="hcl",
            metadata_template=self.metadata_template
        )
        
        tree = builder.parser.parse(bytes(locals_code, "utf8"))
        root_node = tree.root_node
        
        self.assertFalse(root_node.has_error)
        
    def test_terraform_module_block_parsing(self):
        """Test parsing Terraform module blocks"""
        module_code = '''
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  
  name = "my-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]
}
'''
        builder = ASTChunkBuilder(
            max_chunk_size=self.max_chunk_size,
            language="terraform",
            metadata_template=self.metadata_template
        )
        
        tree = builder.parser.parse(bytes(module_code, "utf8"))
        root_node = tree.root_node
        
        self.assertFalse(root_node.has_error)
        
    def test_both_languages_use_same_parser(self):
        """Test that both 'hcl' and 'terraform' languages can parse the same code"""
        hcl_builder = ASTChunkBuilder(
            max_chunk_size=self.max_chunk_size,
            language="hcl",
            metadata_template=self.metadata_template
        )
        
        terraform_builder = ASTChunkBuilder(
            max_chunk_size=self.max_chunk_size,
            language="terraform",
            metadata_template=self.metadata_template
        )
        
        # Parse the same code with both parsers
        hcl_tree = hcl_builder.parser.parse(bytes(self.sample_terraform_code, "utf8"))
        terraform_tree = terraform_builder.parser.parse(bytes(self.sample_terraform_code, "utf8"))
        
        # Both should successfully parse
        self.assertFalse(hcl_tree.root_node.has_error)
        self.assertFalse(terraform_tree.root_node.has_error)


if __name__ == '__main__':
    unittest.main()
