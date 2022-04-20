def tree_walk(data, comment):
    if data['path'] in comment['path'] and len(comment['path']) - len(data['path']) == 4:
        data['children'].append({
            "id": comment['id'],
            "article": comment['article_id'],
            "content": comment['content'],
            "path": comment['path'],
            "children": [],
        })
    else:
        for item in data['children']:
            if len(comment['path']) - len(item['path']) == 4:
                item['children'].append({
                    "id": comment['id'],
                    "article": comment['article_id'],
                    "content": comment['content'],
                    "path": comment['path'],
                    "children": [],
                })
            else:
                item = tree_walk(item, comment)
    return data
