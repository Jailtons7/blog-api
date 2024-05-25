from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def list_blogs():
    return {"msg": "A list of blogs"}


@router.get("/{blog_id}")
async def get_blog(blog_id: int):
    return {"msg": f"A blog of id {blog_id}"}


@router.post("/")
async def post_blog():
    return {"msg": "Created a blog"}


@router.delete("/{blog_id}")
async def delete_blog(blog_id: int):
    return {"msg": "Deleted a blog"}
