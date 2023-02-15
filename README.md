# Role Change Detection Agent

## Description

This agent detects transactions triggering role changes in smart contracts.

## Supported Chains

- Ethereum
- Binance Smart Chain
- Polygon

## Alerts

Describe each of the type of alerts fired by this agent

- ROLE-CHANGE-1
  - Fired when a transaction to a contract invokes a function call that appears to trigger a role change
  - Severity is always set to "low"
  - Type is always set to "info"s
  - Metadata includes the key words used to trigger the alert, as well as the function call invoked in the transaction

## Test Data

The agent behaviour can be verified with the following transactions:

- 0x30a332902920cb6886281f6d28abfa5775559647eb7288e7cc00763fe4427f7b (calls setMetadataManager(address))
