# Copyright 2019 The resource-policy-evaluation-library Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


package gcp.container.projects.locations.clusters.policy.cos_image_used

#####
# Resource metadata
#####

labels = input.labels

#####
# Policy evaluation
#####

default valid = false

# Check if COS image is being used
valid = true {
  invalid_nodepools := [name | input.nodePools[p].config.imageType != "COS"; name := input.nodePools[p].name]
  count(invalid_nodepools) == 0
}

# Check for a global exclusion based on resource labels
valid = true {
  data.exclusions.label_exclude(labels)
}

#####
# Remediation
#####

remediate = {
  "_remediation_spec": "v2beta1",
  "steps": use_cos_image
}

# iterate steps over invalid nodePools (can be updated one at a time)
use_cos_image = result {
  result := { combined | combined := {
      "method": "update",
      "params": {
        "name": combinedName,
        "body": {
          "update": {
            "desiredNodePoolId": _invalid_nodepools[_],
            "desiredImageType": "COS"
          }
        }
      }
    }
  }
}

# define list of nodePools using wrong image types
_invalid_nodepools = invalid_nodepools { invalid_nodepools := [name | input.nodePools[p].config.imageType != "COS"; name := input.nodePools[p].name] }

# break out the selfLink so we can extract the project, region, cluster and name
selfLinkParts = split(input.selfLink, "/")

# create combined resource name
combinedName = sprintf("projects/%s/locations/%s/clusters/%s", [selfLinkParts[5], selfLinkParts[7], selfLinkParts[9]])