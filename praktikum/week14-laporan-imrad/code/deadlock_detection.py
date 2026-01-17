import csv

# ===============================
# Membaca dataset CSV
# ===============================
processes = []
allocation = {}
request = {}

with open("dataset_deadlock.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        p = row["Process"]
        processes.append(p)
        allocation[p] = row["Allocation"]
        request[p] = row["Request"]

# ===============================
# Menampilkan data awal
# ===============================
print("=== Data Proses & Resource ===")
print("Proses | Alokasi | Request")
print("-----------------------------")
for p in processes:
    print(f"{p:<6} | {allocation[p]:<7} | {request[p]}")

# ===============================
# Membangun graf ketergantungan
# ===============================
graph = {}

for p in processes:
    for q in processes:
        if request[p] == allocation[q]:
            graph[p] = q

# ===============================
# Deteksi deadlock (circular wait)
# ===============================
visited = set()
stack = []
deadlock_cycle = []

def dfs(node):
    if node in stack:
        idx = stack.index(node)
        deadlock_cycle.extend(stack[idx:] + [node])
        return True

    if node in visited:
        return False

    visited.add(node)
    stack.append(node)

    if node in graph:
        if dfs(graph[node]):
            return True

    stack.pop()
    return False

deadlock_found = False
for p in processes:
    if dfs(p):
        deadlock_found = True
        break

# ===============================
# Menampilkan hasil
# ===============================
print("\nKondisi Sistem:", end=" ")
if deadlock_found:
    print("DEADLOCK TERDETEKSI")
else:
    print("TIDAK TERJADI DEADLOCK")

print("\n=== Status Proses ===")
print("Proses | Status")
print("-------------------")
for p in processes:
    status = "Terlibat Deadlock" if deadlock_found else "Aman"
    print(f"{p:<6} | {status}")

# ===============================
# Menampilkan circular wait
# ===============================
if deadlock_found:
    print("\nPola Circular Wait:")
    print(" -> ".join(deadlock_cycle))

print("\n==============================")
print("MINI SIMULASI SISTEM OPERASI")
print("==============================")
