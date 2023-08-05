# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Reinforcement Learning CLI Functions"""

import os
import logging

from azureml.contrib.train.rl._rl_runconfig import ReinforcementLearningConfiguration
from azureml._base_sdk_common.cli_wrapper._common import get_workspace_or_default, _get_experiment_or_default
from azureml._cli.run.run_commands import _run_to_output_dict
from azureml._cli.cli_command import _write_output_metadata_file


command_logger = logging.getLogger(__name__)


def run_submit_rl(reinforcement_learning_configuration_name,
                  run_async,
                  verbose,
                  experiment_name=None,
                  subscription_id=None,
                  workspace_name=None,
                  resource_group=None,
                  max_run_duration_seconds=None,
                  cluster_coordination_timeout_seconds=None,
                  path=None,
                  output_metadata_file=None
                  ):
    workspace = get_workspace_or_default(
        subscription_id=subscription_id,
        resource_group=resource_group,
        workspace_name=workspace_name,
        logger=command_logger
    )

    experiment = _get_experiment_or_default(
        workspace=workspace,
        experiment_name=experiment_name,
        logger=command_logger
    )

    if path is None:
        path = os.getcwd()

    command_logger.debug("Workspace : %s ", workspace)
    command_logger.debug("Experiment : %s ", experiment_name)
    command_logger.debug("Resource Group: %s ", resource_group)
    command_logger.debug("Path: %s ", path)

    rl_config = ReinforcementLearningConfiguration.load(path=path, name=reinforcement_learning_configuration_name)

    if max_run_duration_seconds:
        command_logger.info("Overriding rlconfig max run duration seconds %s with %s",
                            rl_config.max_run_duration_seconds,
                            max_run_duration_seconds)
        rl_config.max_run_duration_seconds = max_run_duration_seconds

    if cluster_coordination_timeout_seconds:
        command_logger.info("Overriding rlconfig cluster coordination timeout seconds %s with %s",
                            rl_config.cluster_coordination_timeout_seconds,
                            cluster_coordination_timeout_seconds)
        rl_config.cluster_coordination_timeout_seconds = cluster_coordination_timeout_seconds

    run = experiment.submit(rl_config)

    command_logger.debug("Running asynchronously: %s", run_async)
    if not run_async:
        run.wait_for_completion(show_output=True, wait_post_processing=True)

    return_run_dict = _run_to_output_dict(run)

    if output_metadata_file:
        _write_output_metadata_file(return_run_dict, output_metadata_file, command_logger)

    return return_run_dict, verbose
