from decimal import Decimal


def check_large_transaction(transaction, rule):
    """
    AML-001: Detect transactions at or above the threshold.
    """

    if transaction.amount >= rule.threshold:
        return {
            "triggered": True,
            "rule_code": rule.rule_code,
            "rule_name": rule.rule_name,
            "severity": rule.severity,
            "message": (
                f"Transaction amount {transaction.amount} "
                f"meets or exceeds threshold {rule.threshold}"
            )
        }

    return {
        "triggered": False,
        "rule_code": rule.rule_code
    }


def check_high_frequency(transaction_count, rule):
    """
    AML-002: Detect transaction counts at or above the threshold.
    """

    threshold = int(rule.threshold)

    if transaction_count >= threshold:
        return {
            "triggered": True,
            "rule_code": rule.rule_code,
            "rule_name": rule.rule_name,
            "severity": rule.severity,
            "message": (
                f"Transaction count {transaction_count} "
                f"meets or exceeds threshold {threshold}"
            )
        }

    return {
        "triggered": False,
        "rule_code": rule.rule_code
    }

def check_structuring(total_amount, transaction_count, rule):
    """
    AML-003: Flag a group of transactions that collectively
    reaches the configured threshold.
    """

    if (
        transaction_count > 1
        and Decimal(str(total_amount)) >= rule.threshold
    ):
        return {
            "triggered": True,
            "rule_code": rule.rule_code,
            "rule_name": rule.rule_name,
            "severity": rule.severity,
            "message": (
                f"{transaction_count} transactions total "
                f"{total_amount}, meeting or exceeding "
                f"the threshold {rule.threshold}"
            )
        }

    return {
        "triggered": False,
        "rule_code": rule.rule_code
    }

def check_rapid_fund_movement(elapsed_minutes, rule):
    """
    AML-004: Detect rapid movement of funds through accounts.
    The configured threshold represents minutes.
    """

    elapsed_minutes = Decimal(str(elapsed_minutes))
    threshold = rule.threshold

    if elapsed_minutes <= threshold:
        return {
            "triggered": True,
            "rule_code": rule.rule_code,
            "rule_name": rule.rule_name,
            "severity": rule.severity,
            "message": (
                f"Funds moved through accounts in "
                f"{elapsed_minutes} minutes; "
                f"threshold is {threshold} minutes"
            )
        }

    return {
        "triggered": False,
        "rule_code": rule.rule_code
    }

def check_circular_transfers(cycle_length, rule):
    """
    AML-005: Flag a transfer cycle involving the configured
    minimum number of edges.
    """

    cycle_length = int(cycle_length)
    threshold = int(rule.threshold)

    if cycle_length >= threshold:
        return {
            "triggered": True,
            "rule_code": rule.rule_code,
            "rule_name": rule.rule_name,
            "severity": rule.severity,
            "message": (
                f"Potential circular transfer detected: "
                f"cycle length {cycle_length}, "
                f"threshold {threshold}"
            )
        }

    return {
        "triggered": False,
        "rule_code": rule.rule_code
    }

def check_multiple_counterparties(counterparty_count, rule):
    """
    AML-006: Detect an unusually high number of unique counterparties.
    """

    counterparty_count = int(counterparty_count)
    threshold = int(rule.threshold)

    if counterparty_count >= threshold:
        return {
            "triggered": True,
            "rule_code": rule.rule_code,
            "rule_name": rule.rule_name,
            "severity": rule.severity,
            "message": (
                f"Unique counterparty count {counterparty_count} "
                f"meets or exceeds threshold {threshold}"
            )
        }

    return {
        "triggered": False,
        "rule_code": rule.rule_code
    }

def check_unusual_customer_behavior(
    current_amount,
    historical_mean,
    historical_stddev,
    rule
):
    """
    AML-007: Flag a transaction unusually far from
    the customer's historical average.
    """

    current_amount = Decimal(str(current_amount))
    historical_mean = Decimal(str(historical_mean))
    historical_stddev = Decimal(str(historical_stddev))
    threshold = Decimal(str(rule.threshold))

    if historical_stddev <= 0:
        return {
            "triggered": False,
            "rule_code": rule.rule_code,
            "message": "Insufficient historical variation to calculate deviation"
        }

    deviation = abs(current_amount - historical_mean) / historical_stddev

    if deviation >= threshold:
        return {
            "triggered": True,
            "rule_code": rule.rule_code,
            "rule_name": rule.rule_name,
            "severity": rule.severity,
            "message": (
                f"Transaction is {deviation:.2f} standard deviations "
                f"from the historical average"
            )
        }

    return {
        "triggered": False,
        "rule_code": rule.rule_code
    }

def check_layering_pattern(intermediary_count, rule):
    """
    AML-008: Flag a potential layering pattern involving
    the configured minimum number of intermediary accounts.
    """

    intermediary_count = int(intermediary_count)
    threshold = int(rule.threshold)

    if intermediary_count >= threshold:
        return {
            "triggered": True,
            "rule_code": rule.rule_code,
            "rule_name": rule.rule_name,
            "severity": rule.severity,
            "message": (
                f"Potential layering pattern detected across "
                f"{intermediary_count} intermediary accounts; "
                f"threshold is {threshold}"
            )
        }

    return {
        "triggered": False,
        "rule_code": rule.rule_code
    }