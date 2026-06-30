WTC Private Chain - Setup Guide
================================

E: Drive Free Space: 666 GB
Chain ID: 456789
Gas: FREE (0 gas)

HOW TO SETUP:
===============

STEP 1: Initialize + Start Chain
  Double-click: 1_init_and_start.bat
  - This will init the chain and start the node
  - Keep the cmd window open (it's the node)
  - RPC will be at http://localhost:8545

STEP 2: Deploy WTC Token
  Double-click: 2_deploy_wtc.bat
  - Deploys WTC token to your private chain

STEP 3: MetaMask
  Network Name: WTC Private Chain
  RPC URL: http://223.18.36.147:8545
  Chain ID: 456789
  Currency Symbol: WTC

YOUR ACCOUNTS (have unlimited balance):
  0xcA02C4888D7dfa3f052702b1288cF3eE50F248D7
  0xdffA9CFE9FFA749Fd93883c587193381263AA59c

NOTES:
  - Private chain is only accessible when the CMD window is open
  - If you close the window, the chain stops
  - All balances prefunded, all gas is FREE
