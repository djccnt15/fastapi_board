from ..model import post_response


async def to_post_response(*, data: dict) -> post_response.PostResponse:
    post_entity = vars(data.get("PostEntity"))

    post_id = post_entity.get("id", None)
    created_datetime = post_entity.get("created_datetime", None)
    updated_datetime = data.get("created_datetime", None)
    category = vars(data.get("PostCategoryEntity")).get("name", None)
    user = vars(data.get("UserEntity")).get("name", None)
    title = data.get("title", None)
    content = data.get("content", None)

    res = post_response.PostResponse(
        id=post_id,
        created_datetime=created_datetime,
        updated_datetime=updated_datetime,
        category=category,
        user=user,
        title=title,
        content=content,
    )
    return res
