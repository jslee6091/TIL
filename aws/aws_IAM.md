### AWS IAM

- 자격을 인증하고 권한을 부여
- AWS 고객이 AWS 계정 및 AWS 내에서 사용 가능한 API 및 서비스에 대한 사용자의 액세스 및 권한을 관리할 수 있도록 하는 서비스
- 사용자, 보안 자격 증명(예: API Access Key)을 관리하고 사용자가 AWS 리소스에 액세스할 수 있도록 허용할 수 있음



![img](aws_basic.assets/0P2PYubD4vHvlJRaWKQowF8-80N1D8sipV3X1QJ4v3pJHIeCnJ2o2w_1aT63vD9oCdeq4V6CnMowQaYmxKMqBFrSKlWILTWyjAUqx-bzQbJneBf1CJC3z0SKWIwTozmc8ZFDW2CU)



### IAM 정책

```json
{
    "Version": "2012-10-17", 
    "Statement": [				⇐ 정책 문서
        {
            "Resource": "*", 	⇐ 자원
            "Action": "*", 		⇐ 작업
            "Effect": "Allow"	⇐ 효과 = 리소스에 대한 작업의 허용 여부를 명시
        }
    ]
}
```



- S3-Support Group에 적용되어 있는 정책

  - ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "s3:Get*",
            "s3:List*"
          ],
          "Resource": "*"
        }
      ]
    }
    ```

- EC2-Support Group에 적용되어 있는 정책

  - ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": "ec2:Describe*",
          "Resource": "*"
        },
        {
          "Effect": "Allow",
          "Action": "elasticloadbalancing:Describe*",
          "Resource": "*"
        },
        {
          "Effect": "Allow",
          "Action": [
            "cloudwatch:ListMetrics",
            "cloudwatch:GetMetricStatistics",
            "cloudwatch:Describe*"
          ],
          "Resource": "*"
        },
        {
          "Effect": "Allow",
          "Action": "autoscaling:Describe*",
          "Resource": "*"
        }
      ]
    }
    ```

- EC2-Admin Group에 적용되어 있는 정책

  - ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Action": [
            "ec2:Describe*",
            "ec2:StartInstances",
            "ec2:StopInstances"
          ],
          "Resource": "*",
          "Effect": "Allow"
        },
        {
          "Action": "elasticloadbalancing:Describe*",
          "Resource": "*",
          "Effect": "Allow"
        },
        {
          "Action": [
            "cloudwatch:ListMetrics",
            "cloudwatch:GetMetricStatistics",
            "cloudwatch:Describe*"
          ],
          "Resource": "*",
          "Effect": "Allow"
        },
        {
          "Action": "autoscaling:Describe*",
          "Resource": "*",
          "Effect": "Allow"
        }
      ]
    }
    ```

  - 

