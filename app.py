import panel as pn
from database import Database

db = Database()
db.connect()

pn.extension("codeeditor")

pn.extension(sizing_mode="stretch_width", design="material")

BUTTON_WIDTH = 125

snippets = pn.Column(scroll=True, height=300)

title_text_input = pn.widgets.TextInput(name="Title", placeholder="Snippet Title")

language_select = pn.widgets.Select(
    name="Language", options=["python", "javascript", "java"]
)

add_snippet_editor = pn.widgets.CodeEditor(
    language=language_select,
    theme="monokai",
    name="add-snippet-editor",
)

update_snippet_editor = pn.widgets.CodeEditor(
    name="update-snippet-editor",
    theme="monokai",
)

update_snippet_column = pn.Column()


def can_add(value_input, editor_input):
    return not bool(value_input) or not bool(editor_input)


def can_update(value_input, original, *args):
    return False if bool(value_input) and value_input != original else True


def update_snippet(code_compare, *args):
    snippet_id, original = (
        code_compare["snippet_id"],
        code_compare["original"],
    )
    if original != update_snippet_editor.value:
        db.update_snippet(snippet_id, update_snippet_editor.value)


submit_snippet = pn.widgets.Button(
    align="center",
    icon="device-floppy",
    sizing_mode="fixed",
    disabled=pn.bind(
        can_add, title_text_input.param.value_input, add_snippet_editor.param.value
    ),
)


def remove_snippet(snippet_data, *args):
    snippet_row, loaded_snippet = (
        snippet_data["snippet_row"],
        snippet_data["loaded_snippet"],
    )
    snippet_id, title, language, code = (
        loaded_snippet["snippet_id"],
        loaded_snippet["title"],
        loaded_snippet["language"],
        loaded_snippet["code"],
    )
    if bool(update_snippet_column) and update_snippet_column[0].object == title:
        update_snippet_column.clear()
    db.delete_snippet(snippet_id)
    index = snippets.index(snippet_row)
    snippets.pop(index)


def create_snippet(*args):
    title = title_text_input.value.strip()
    language = language_select.value
    code = add_snippet_editor.value.strip()
    if title not in [
        row[0].object for row in snippets if isinstance(row[0], pn.pane.Markdown)
    ]:
        new_snippet = db.create_snippet(title, language, code)
        new_title = new_snippet["title"]
        title_text_input.value = ""
        add_snippet_editor.value = ""
        if bool(new_title):
            return add_snippet(new_snippet)


def show_update_editor(snippet, *args):
    update_snippet_column.clear()
    snippet_id, title, language, code = (
        snippet["snippet_id"],
        snippet["title"],
        snippet["language"],
        snippet["code"],
    )

    update_snippet_button = pn.widgets.Button(
        name="Update",
        align="center",
        button_type="primary",
        width=BUTTON_WIDTH,
        sizing_mode="fixed",
        disabled=pn.bind(can_update, update_snippet_editor.param.value_input, code),
    )

    code_compare = {
        "original": code,
        "snippet_id": snippet_id,
    }

    update_snippet_editor.value = code
    update_snippet_editor.language = language

    pn.bind(update_snippet, code_compare, update_snippet_button, watch=True)

    update_snippet_column.append(f"## {language}: *{title}*")
    update_snippet_column.append(update_snippet_editor)
    update_snippet_column.append(pn.Row(update_snippet_button))


def add_snippet(loaded_snippet, *args):
    title = loaded_snippet["title"]
    show = pn.widgets.Button(
        # name=f"show-{title}-btn",
        # id=f"show-{title}-btn",
        icon="folder",
        sizing_mode="fixed",
    )
    content = pn.pane.Markdown(title)
    remove = pn.widgets.Button(icon="trash", sizing_mode="fixed")
    title_row = pn.Row(content, show, remove, sizing_mode="stretch_width")

    snippet_data = {
        "snippet_row": title_row,
        "loaded_snippet": loaded_snippet,
    }

    pn.bind(show_update_editor, loaded_snippet, show, watch=True)
    pn.bind(remove_snippet, snippet_data, remove, watch=True)

    snippets.append(title_row)

    return snippets


def load_snippets():
    db.list_snippets()
    loaded_snippets = db.list_snippets()
    for snippet in loaded_snippets:
        add_snippet(snippet)


load_snippets()

pn.bind(
    create_snippet,
    submit_snippet,
    watch=True,
)

gridspec = pn.GridSpec(sizing_mode="stretch_both", max_height=800)
gridspec[0, 0] = pn.Column(
    "## Snippets",
    snippets,
)
gridspec[0, 1:] = pn.Column(
    pn.Row(title_text_input, language_select, submit_snippet),
    add_snippet_editor,
)
gridspec[1, :3] = update_snippet_column
pn.Column(gridspec).servable()
