terraform {
  source = "../../../modules//cluster"
}

include {
  path = find_in_parent_folders()
}

dependency "initbuild" {
    config_path = "../initbuild"
}

dependency "ecr" {
    config_path = "../ecr"
    mock_outputs = {
      ecr_repository_url = "000000000000.dkr.ecr.eu-west-1.amazonaws.com/image"
  }
}

inputs = {
    ecr_repository_url = dependency.ecr.outputs.ecr_repository_url
    ssm_db_pass_name  = dependency.initbuild.outputs.ssm_db_pass_name
}