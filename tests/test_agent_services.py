from dgm_contracts import (
    NullAgentLogger,
    NullProviderService,
    NullTaskService,
)


def test_null_agent_services_are_standalone():
    logger = NullAgentLogger()
    logger.info("info")
    logger.error("error")
    logger.critical("critical")

    NullProviderService().run()
    NullTaskService().analyze_issue("repo", "test")
