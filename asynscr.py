import asyncio
import aiohttp
import hashlib
import os

async def download_repo(url: str, folder: str) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                repo_content = await response.read()
                with open(os.path.join(folder, 'repo_content'), 'wb') as f:
                    f.write(repo_content)

# async def calculate_sha256(folder: str) -> None:
#     for file_name in os.listdir(folder):
#         file_path = os.path.join(folder, file_name)
#         if os.path.isfile(file_path):
#             with open(file_path, 'rb') as f:
#                 file_content = f.read()
#                 file_sha256 = hashlib.sha256(file_content).hexdigest()
#                 print(f"{file_name}: {file_sha256}")
async def calculate_sha256(folder):
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    for file in files:
        file_path = os.path.join(folder, file)
        with open(file_path, 'rb') as f:
            content = f.read()
            sha256_hash = hashlib.sha256(content).hexdigest()
            print(f"{file}: {sha256_hash}")

async def main() -> None:
    temp_folder = 'temp'
    os.makedirs(temp_folder, exist_ok=True)
    tasks = []
    for i in range(3):
        task = asyncio.create_task(download_repo('https://gitea.radium.group/radium/project-configuration.git', temp_folder))
        tasks.append(task)
    await asyncio.gather(*tasks)
    await calculate_sha256(temp_folder)

if __name__ == '__main__':
    asyncio.run(main())
