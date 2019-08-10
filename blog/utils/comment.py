
def comment_tree(comment_list):
    """
    后端处理多级评论
    :param result: [ {id,:child:[xxx]},{}]
    :return:
    """
    comment_str = "<div class='comment'>"
    for row in comment_list:
        tpl = "<div class='content'>%s</div>" %(row['content'])
        comment_str += tpl
        if row['child']:
            #
            child_str = comment_tree(row['child'])
            comment_str += child_str
    comment_str += "</div>"

    return comment_str