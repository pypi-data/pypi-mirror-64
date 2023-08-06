import boto3
from botocore.exceptions import ClientError
import sys
from pprint import pformat


class Cfn:
    def __init__(self, logger):
        """Description:
            Convenience Python module for AWS CloudFormation

        Args:
            logger (onnlogger.Loggers): An instance of `onnlogger.Loggers`

        Example:
            Example usage:

                from onnlogger import Loggers
                logger = Loggers(logger_name='Orgs', console_logger=True, log_level='INFO', log_file_path='/tmp/log')
                cfn = Cfn(logger)
        """
        self.logger = logger
        self.default_cfn_client = boto3.client('cloudformation')

    def dict_to_cfn_params(self, dict_params) -> list:
        """Description:
            Converts a `dict` to CloudFormation parameters

        Args:
            dict_params: Dictionary that needs to be converted to CloudFormation parameters

        Example:
            Example usage:

                params = {
                    'AccountId': '123456789012',
                    'ExternalId': '098765432109',
                    }

                cfn_params = cfn.dict_to_cfn_params(params)
                pprint(cfn_params)
                [{'ParameterKey': 'AccountId', 'ParameterValue': '123456789012'},
                {'ParameterKey': 'ExternalId', 'ParameterValue': '098765432109'}]

        Returns:
            List of CloudFormation parameters
        """
        self.logger.entry('info', f'Converting dict params to CloudFormation params...')
        self.logger.entry('debug', f'Dict params:\n{pformat(dict_params)}')
        cfn_params = []

        for key, value in dict_params.items():
            entry = {
                'ParameterKey': key,
                'ParameterValue': value,
            }

            cfn_params.append(entry)

        self.logger.entry('debug', f'CloudFormation params:\n{pformat(cfn_params)}')
        return cfn_params

    def create_stack(self, cfn_settings, cfn_client=None):
        """Description:
            Creates a CloudFormation stack

        Args:
            cfn_settings (dict): [`create_stack`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.create_stack) request parameters
            cfn_client: (Optional) `cloudformation` client - used for assumed roles

        Example:
            Example usage:

                params = {
                    'AccountId': account_id,
                    'ExternalId': org_id,
                }

                cfn_params = self.onn_cfn.dict_to_cfn_params(params)

                cfn_settings = {
                    'StackName': STACK_NAME,
                    'TemplateURL': TEMPLATE_URL,
                    'Parameters': cfn_params,
                    'Capabilities': ['CAPABILITY_NAMED_IAM'],
                }

                result = self.onn_cfn.create_stack(cfn_settings)
                pprint(result)
                {'ResponseMetadata': {'HTTPHeaders': {'content-length': '385',
                                          'content-type': 'text/xml',
                                          'date': 'Fri, 27 Mar 2020 04:21:24 GMT',
                                          'x-amzn-requestid': '457fg2347fd-2353-32g4-dfsk93jha1'},
                          'HTTPStatusCode': 200,
                          'RequestId': '457fg2347fd-2353-32g4-dfsk93jha1',
                          'RetryAttempts': 0},
                'StackId': 'arn:aws:cloudformation:us-east-1:123456789012:stack/StackName/'457fg2347fd-2353-32g4-dfsk93jha1'}

        Returns:
            [`create_stack`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.create_stack) response or `False` if a template with this name already exists

        """
        cfn_client = cfn_client if cfn_client else self.default_cfn_client

        stack_name = cfn_settings['StackName']
        self.logger.entry('info', f'Creating "{stack_name}" stack...')

        try:
            stack_details = cfn_client.create_stack(**cfn_settings)
            self.logger.entry('debug', f'Stack details:\n{pformat(stack_details)}')

            return stack_details

        except ClientError as e:
            msg = e.response['Error']['Message']
            if 'already exists' in msg:
                self.logger.entry('info', f'Stack "{stack_name}" already exists')

                return False

            else:
                self._aws_exception_msg(e)

    def waiter(self, wait_for_status, cfn_client=None):
        """Description:
            CloudFormation waiter

        Args:
            wait_for_status: Wait for status, e.g `stack_create_complete`
            cfn_client: (Optional) `cloudformation` client - used for assumed roles

        Example:
            Example usage:

            cfn.waiter(wait_for_status='stack_create_complete')

        Returns:
            None

        """
        cfn_client = cfn_client if cfn_client else self.default_cfn_client

        try:
            waiter = cfn_client.get_waiter(wait_for_status)
            waiter.wait()

        except ClientError as e:
            self._aws_exception_msg(e)

    @staticmethod
    def _aws_exception_msg(e):
        msg = e.response['Error']['Message']
        sys.exit(f'Error: {msg}')

    def outputs_to_dict(self, cfn_id, cfn_client=None):
        """

        Args:
            cfn_id: CloudFormation ID from which to extract the outputs
            cfn_client: (Optional) `cloudformation` client - used for assumed roles

        Example:
            Example usage:

                cfn_outputs = cfn.outputs_to_dict(cfn_id)
                pprint(cfn_outputs)
                {'Hostname': 'TestHost',
                'Version': '1.18'}

        Returns:
            CloudFormation outputs as a dictionary
        """
        self.logger.entry('debug', 'Converting CloudFormation outputs to dict...')
        cfn_client = cfn_client if cfn_client else self.default_cfn_client

        cfn_details = cfn_client.describe_stacks(StackName=cfn_id)
        cfn_outputs = cfn_details['Stacks'][0]['Outputs']
        self.logger.entry('debug', f'CloudFormation outputs:\n{pformat(cfn_outputs)}')

        output = {}
        for entry in cfn_outputs:
            key = entry['OutputKey']
            value = entry['OutputValue']
            output[key] = value

        self.logger.entry('debug', f'Dict outputs:\n{pformat(output)}')
        return output
