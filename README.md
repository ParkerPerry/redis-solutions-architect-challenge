Redis Solutions Architect Challenge

This project demonstrates a simple shopping cart application built using Redis, in response to the Redis Solutions Architect technical challenge. It includes user management, SKU/item tracking, and cart manipulation. The app connects to a local Redis instance and is fully visualized using Redis Insight.

⸻

🧱 Features
   •  Create and view users stored in Redis Hashes
   •  Add, remove, and view SKUs (items)
   •  Add/remove items from shopping carts with support for quantities
   •  Calculate dynamic totals per cart
   •  Insert and read 10,000 sequential values from a Redis List using pipelining
   •  Inspect and interact with Redis data using Redis Insight

⸻

🚀 Getting Started

1. Install Redis (Community Edition)

If you haven’t already:

brew tap redis/redis
brew install --cask redis

Start the server:

redis-server /opt/homebrew/etc/redis.conf

2. Install Python Requirements

pip install redis

3. Run the App

python3 shopping_cart.py



⸻

🖥️ Note on Server A / Server B

The challenge instructions reference Server A for inserting values and Server B for reading them in reverse. In this proof of concept, both roles are simulated on a single local Redis instance for simplicity.

In a production environment, Server A would likely be an ingestion or application service writing data to Redis (e.g., using pipelines), while Server B could represent a separate analytics or consumer service — potentially connecting to Redis Enterprise in a cloud environment like Azure. For this demo, insertion and consumption are logically separated in code, but executed locally for reproducibility.

⸻

🔍 Redis Insight Instructions
   1. Download Redis Insight from redis.io/docs/ui/insight
   2. Launch it and add a connection:
   •  Host: 127.0.0.1
   •  Port: 6379
   3. Use the “Keys Browser” to view:
   •  user:1 (Hash)
   •  cart:1 (Hash)
   •  sku:sku123, sku:sku456 (Hashes)
   •  biglist (List of 10,000 inserted integers)
   4. 📸 Take a screenshot of this view for submission.

⸻

📥 Insert & Read 10,000 Values in Reverse (Server A/B Simulation)

The application includes logic to insert 10,000 sequential integers into a Redis List (biglist) using LPUSH and a pipeline for efficient bulk insertion. It then reads them back in reverse (original ascending) order using LRANGE.

🧠 This simulates a real-world “Server A / Server B” scenario:
   •  Server A: Inserts data (modeled by insert_large_list())
   •  Server B: Reads and prints data (modeled by read_list_reverse())

💡 For simplicity and reproducibility, both operations are run locally in the same script.

Sample Output:

Inserted 1 to 10,000 into 'biglist'.

First 10 values in reverse (original) order:
['10000', '9999', '9998', '9997', '9996', '9995', '9994', '9993', '9992', '9991']

You can view this biglist directly in Redis Insight to validate structure and order.

⸻

📊 Scaling Thoughts

To support hundreds of millions of inserts:
   •  Use Redis pipelining to batch commands efficiently
   •  Leverage multithreaded or async clients
   •  Partition large lists or hashes across user IDs
   •  Use Redis Streams or pub/sub for real-time consumption across distributed consumers

⸻

☁️ Azure Managed Redis (Optional)

1. Provision & Connect

Using your Azure account, create a Redis Enterprise database via Azure Managed Redis (Enterprise Tier). Then connect it to Redis Insight using the public hostname and access key provided in the Azure portal.

2. Create a Hash in Redis Insight

In Redis Insight, manually create a Hash with key user:1, and fields:
   •  firstname: "Parker"
   •  lastname: "Perry"

This simulates user creation directly inside AMR, similar to your app’s behavior.

3. AMR vs. ElastiCache (3-Sentence Summary)

Azure Managed Redis (AMR) includes Redis Enterprise features like Redis modules, active-active geo-replication, and better integration with Azure-native services. AWS ElastiCache offers high performance, multi-AZ support, and IAM security, but does not support Redis modules in most regions. AMR is preferred for enterprise workloads that need the full Redis Enterprise feature set, especially in Microsoft environments.

⸻

📁 File Overview

shopping_cart.py       # Main Python application (includes shopping cart + 10,000 value logic)
README.md              # This file



⸻

📸 Screenshots (Optional)
   •  Redis Insight view showing cart, SKUs, and user data
   •  Redis Insight view of biglist with 10,000 inserted values

⸻

✅ Submission Checklist
   •  Redis installed and running locally
   •  Redis Insight connected and visualized
   •  Python app demonstrating user + cart behavior
   •  Screenshot(s) from Redis Insight
   •  Optional AMR demo (if completed)
   •  GitHub repo with this README

⸻

🙌 Author

Parker Perry
Redis Solutions Architect Technical Challenge