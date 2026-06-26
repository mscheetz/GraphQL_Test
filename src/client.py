import httpx
import asyncio

GRAPHQL_URL = "http://127.0.0.1:8000/graphql"

async def run_query(query: str, variables: dict | None = None):
    async with httpx.AsyncClient() as client:
        response = await client.post(            
            GRAPHQL_URL,
            json={
                "query": query,
                "variables": variables or {}
            }
        )

    response.raise_for_status()
    return response.json()

async def run_print_query(query: str, variables: dict | None = None):
    result = await run_query(query, variables)

    print(result)

async def get_authors():
    query = """
    query {
        authors {
            id
            name
        }
    }
    """

    await run_print_query(query)

async def get_books():
    query = """
    query {
        books {
            id
            title
            author {
                id
                name
            }
        }
    }
    """

    await run_print_query(query)

async def add_author(name: str):
    query = """
    mutation AddAuthor($name: String!) {
        addAuthor(name: $name) {
            success
            message
            author {
                id
                name
            }
        }
    }
    """

    await run_print_query(query, {"name": name})

async def add_book(title: str, author_id: int):
    query = """
    mutation AddBook($title: String!, $author_id: Int!) {
        addBook(title: $title, authorId: $author_id) {
            success
            message
            book {
                id
                title
                author {
                    name
                }
            }
        }
    }
    """

    await run_print_query(query, { "title": title, "author_id": author_id})

async def main():

    print("## GET AUTHORS ##")
    await get_authors()

    print("## GET BOOKS ##")
    await get_books()

    print("## ADD AUTHOR (1/2) ##")
    await add_author("Mario Puzo")

    print("## ADD AUTHOR (2/2) ##")
    await add_author("Mario Puzo")

    print("## ADD BOOK (1/3) ##")
    await add_book("The Godfather", 7)

    print("## ADD BOOK (2/3) ##")
    await add_book("The Godfather", 3)

    print("## ADD BOOK (3/3) ##")
    await add_book("The Godfather", 3)

if __name__ == "__main__":
    asyncio.run(main())
