import asyncio
import random
import logging
import os
from web3 import Web3
from datetime import datetime, timedelta

# Load RPC URL and Contract Address from environment variables or use defaults
RPC_URL = os.getenv("RPC_URL", "https://rpc.zora.energy")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS", "")
METHOD_ID = '0x'  # Method ID for the transaction

# Web3 setup
web3 = Web3(Web3.HTTPProvider(RPC_URL))

# Load private keys from file
with open("pvkey.txt", "r") as file:
    private_keys = [line.strip() for line in file if line.strip()]

# Initialize nonces dynamically based on current blockchain state
nonces = {key: web3.eth.get_transaction_count(web3.eth.account.from_key(key).address) for key in private_keys}

# Set up logging to file
logging.basicConfig(filename="transactions.log", level=logging.INFO, format="%(asctime)s - %(message)s")

async def handle_eth_transactions(amount_eth, transaction_number, day_number):
    global nonces
    amount_wei = web3.to_wei(amount_eth, 'ether')

    for private_key in private_keys:
        from_address = web3.eth.account.from_key(private_key).address
        short_from_address = from_address[:4] + "..." + from_address[-4:]
        retries = 3  # Number of retries for failed transactions

        for attempt in range(retries):
            try:
                # Re-fetch nonce to ensure it's accurate
                current_nonce = web3.eth.get_transaction_count(from_address)
                
                # Create the transaction
                transaction = {
                    'to': CONTRACT_ADDRESS,
                    'value': amount_wei,
                    'gas': 100000,
                    'gasPrice': web3.eth.gas_price,
                    'nonce': current_nonce,
                    'data': METHOD_ID
                }

                signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)
                tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

                # Log and print transaction details
                log_message = f"[Day {day_number}] Transaction {transaction_number} sent from {short_from_address} with hash: {tx_hash.hex()} at {datetime.utcnow()} and amount: {amount_eth:.8f} ETH"
                logging.info(log_message)
                print(log_message)

                # Increment nonce after successful transaction
                nonces[private_key] = current_nonce + 1
                await asyncio.sleep(random.uniform(1, 5))  # Random delay between 1 to 5 seconds
                break  # Exit retry loop on success

            except Exception as e:
                if 'nonce too low' in str(e):
                    logging.warning(f"Nonce too low for {short_from_address}. Fetching the latest nonce...")
                    nonces[private_key] = web3.eth.get_transaction_count(from_address)
                elif attempt < retries - 1:
                    logging.warning(f"Error sending transaction from {short_from_address}: {str(e)}. Retrying...")
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logging.error(f"Failed to send transaction after {retries} attempts: {str(e)}")

async def run_daily_transactions(num_transactions, num_days):
    # Set a constant amount to send
    constant_amount_eth = 0.00000001  # Fixed amount in ETH

    for day in range(num_days):
        start_time = datetime.utcnow().replace(hour=7, minute=0, second=0, microsecond=0) + timedelta(days=day)
        end_time = datetime.utcnow().replace(hour=18, minute=0, second=0, microsecond=0) + timedelta(days=day)

        print(f"Day {day + 1}/{num_days} - Transactions will start at {start_time.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        logging.info(f"Day {day + 1}/{num_days} - Transactions will start at {start_time.strftime('%Y-%m-%d %H:%M:%S')} UTC")

        # Wait until the start time
        while datetime.utcnow() < start_time:
            await asyncio.sleep(1)

        # Calculate total duration for the transactions
        total_duration = (end_time - start_time).total_seconds()
        average_delay = total_duration / num_transactions

        for i in range(num_transactions):
            # Random delay around the average delay
            delay = random.uniform(0.8 * average_delay, 1.2 * average_delay)  # ±20% of average delay
            print(f"[Day {day + 1}] Waiting {delay:.2f} seconds before transaction {i + 1}/{num_transactions}")
            await asyncio.sleep(delay)

            # Use the constant amount for transactions
            amount_eth = constant_amount_eth
            await handle_eth_transactions(amount_eth, i + 1, day + 1)

        print(f"End of transactions for day {day + 1}. Waiting for the next day...")
        logging.info(f"End of transactions for day {day + 1}. Waiting for the next day...")

async def main():
    try:
        num_transactions = int(input("Enter the number of transactions to execute each day: "))
        if num_transactions <= 0:
            raise ValueError("Number of transactions must be positive.")

        num_days = int(input("Enter the number of days to run the program: "))
        if num_days <= 0:
            raise ValueError("Number of days must be positive.")

    except ValueError as e:
        logging.error(f"Invalid input: {e}")
        return

    await run_daily_transactions(num_transactions, num_days)

if __name__ == '__main__':
    asyncio.run(main())
