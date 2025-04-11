# Redis Solutions Architect Challenge

This project demonstrates a simple shopping cart application built using Redis. It includes user management, SKU/item tracking, cart manipulation, and a performance demo for inserting and reading large volumes of data. The app connects to a local Redis instance and is fully visualized using Redis Insight.

⸻

## 🧱 Features
- Create and view users stored in Redis Hashes
- Add, remove, and view SKUs (items)
- Add/remove items from shopping carts with support for quantities
- Calculate dynamic totals per cart
- Insert and read 10,000 sequential values from a Redis List using pipelining
- Inspect and interact with Redis data using Redis Insight

⸻

## 🧱 Data Model Overview

This application models a shopping cart system using Redis native data structures optimized for speed and flexibility. The design supports multi item carts, SKU tracking, and user linkage.

### 🔑 Key Structure

| Redis Key         | Data Type | Description                                   |
|-------------------|-----------|-----------------------------------------------|
| `user:{user_id}`  | Hash      | Stores user profile fields like name          |
| `sku:{sku_id}`    | Hash      | Represents individual SKUs with name & price  |
| `cart:{user_id}`  | Hash      | Maps SKU IDs to quantities for a user's cart  |
| `biglist`         | List      | Holds integers from 1 to 10,000 (performance demo) |

### 📦 Example

```
user:1         → { first_name: "Parker", last_name: "Perry" }
sku:sku123     → { name: "AirPods", price: "199.99" }
cart:1         → { sku123: "2", sku456: "1" }
biglist        → [10000, 9999, 9998, ..., 1]
```

### 💡 Why This Works
- **Scalable**: Hashes let you store an arbitrary number of SKUs per cart
- **Flexible**: Quantity updates are efficient via `HINCRBY`
- **Fast**: All reads and writes are constant time operations (O(1))
- **Real World Ready**: Pattern maps well to production Redis backed systems

⸻

## 🚀 Getting Started

### 1. Install Redis (Community Edition)
If you haven’t already:

```bash
brew tap redis/redis
brew install --cask redis
```

Start the server:

```bash
redis-server /opt/homebrew/etc/redis.conf
```

### 2. Install Python Requirements

```bash
pip install redis
```

### 3. Run the App

```bash
python3 shopping_cart.py
```

⸻

## 🖥️ Note on Server A / Server B

The challenge instructions reference Server A for inserting values and Server B for reading them in reverse. In this proof of concept, both roles are simulated on a single local Redis instance for simplicity.

In a production environment, Server A would likely be an ingestion or application service writing data to Redis (e.g., using pipelines), while Server B could represent a separate analytics or consumer service — potentially connecting to Redis Enterprise in a cloud environment like Azure. For this demo, insertion and consumption are logically separated in code, but executed locally for reproducibility.

⸻

## 🔍 Redis Insight Instructions

1. Download Redis Insight from https://redis.io/docs/ui/insight
2. Launch it and add a connection:
   - Host: 127.0.0.1
   - Port: 6379
3. Use the “Keys Browser” to view:
   - `user:1` (Hash)
   - `cart:1` (Hash)
   - `sku:sku123`, `sku:sku456` (Hashes)
   - `biglist` (List of 10,000 inserted integers)
4. 📸 Screenshots of the view for submission.

⸻

## 📥 Insert & Read 10,000 Values in Reverse (Server A/B Simulation)

The application includes logic to insert 10,000 sequential integers into a Redis List (`biglist`) using `LPUSH` and a pipeline for efficient bulk insertion. It then reads them back in reverse (original ascending) order using `LRANGE`.

### 🧠 This simulates a real world “Server A / Server B” scenario:
- **Server A**: Inserts data (modeled by `insert_large_list()`)
- **Server B**: Reads and prints data (modeled by `read_list_reverse()`)

For simplicity and reproducibility, both operations are run locally in the same script.

#### Sample Output

```
Inserted 1 to 10,000 into 'biglist'.

First 10 values in reverse (original) order:
['10000', '9999', '9998', '9997', '9996', '9995', '9994', '9993', '9992', '9991']
```

You can view this `biglist` directly in Redis Insight to validate structure and order.

⸻

## 🧠 High Volume Insertion & Consumption Strategy

To insert hundreds of millions of values efficiently using multiple threads and clients:

1. **Use Redis Pipelining**  
Group multiple Redis commands into a single network request to reduce round trip latency. This dramatically improves write throughput.

2. **Leverage Connection Pooling & Multithreading**  
Use Redis clients that support connection pooling (e.g., redis py’s `ConnectionPool`) across multiple threads or async workers. This allows concurrent writes across multiple producers.

3. **Distribute Writes Across Shards or Key Patterns**  
Rather than inserting all data into a single Redis list (which may become a bottleneck), partition data across multiple keys (e.g., `list:shard:1`, `list:shard:2`, …). You can then merge these in reads or use a Redis Cluster to scale horizontally.

4. **Choose the Right Data Type for Consumption Pattern**  
- For a pure append only workload with reverse reads, `LPUSH` + `LRANGE` is ideal.  
- For real time consumption by multiple clients, consider using Redis Streams or Pub/Sub to fan out inserts and allow independent consumers.

5. **Consumer Side Reverse Reads**  
When reading, use `LRANGE 0 -1` and iterate the list client side in reverse, or use a descending index pattern (`LRANGE -10 -1`) depending on the use case.

6. **Consider Redis Enterprise or Redis on Flash**  
At massive scale (billions of entries), memory capacity becomes a concern. Redis Enterprise or Redis on Flash can help reduce RAM pressure while retaining performance.

⸻

## ☁️ Azure Managed Redis (Optional)

### 1. Provision & Connect

Using your Azure account, create a Redis Enterprise database via Azure Managed Redis (Enterprise Tier). Then connect it to Redis Insight using the public hostname and access key provided in the Azure portal.

### 2. Create a Hash in Redis Insight

In Redis Insight, manually create a Hash with key `user:1`, and fields:
- `firstname`: "Parker"
- `lastname`: "Perry"

This simulates user creation directly inside AMR, similar to your app’s behavior.

### 3. AMR vs. ElastiCache (3 Sentence Summary)

Azure Managed Redis (AMR) includes Redis Enterprise features like Redis modules, active/active geo replication, and better integration with Azure native services. AWS ElastiCache offers high performance, multi AZ support, and IAM security, but does not support Redis modules in most regions. AMR is preferred for enterprise workloads that need the full Redis Enterprise feature set, especially in Microsoft environments.

⸻

## 📁 File Overview
```
shopping_cart.py       # Main Python application (includes shopping cart + 10,000 value logic)
README.md              # This file
```

⸻

## 📸 Screenshots:
- Redis Insight view showing cart, SKUs, and user data
- Redis Insight view of biglist with 10,000 inserted values

⸻

## ✅ Submission Checklist
- [x] Redis installed and running locally
- [x] Redis Insight connected and visualized
- [x] Python app demonstrating user + cart behavior
- [x] Screenshot(s) from Redis Insight
- [x] Optional AMR demo (if completed)
- [x] GitHub repo with this README

⸻

## 🙌 Author
**Parker Perry**  
Redis Solutions Architect Technical Challenge


⸻

