extends CenterContainer

var current_item: Node = null
var used_items := []
var used_items_names := PoolStringArray()

onready var grid_container := $GridContainer as GridContainer


func _ready() -> void:
	inventory = grid_container.get_children()
	for i in inventory.size():
		var child = inventory[i]
		child.connect("mouse_entered", self, "set_current_item", [child])
		child.connect("mouse_exited", self, "set_current_item", [null])
		child.connect("used", self, "_on_item_used")
	if get_tree().get_current_scene() == self:
		_run()

func _input(event: InputEvent) -> void:
	if event is InputEventMouseButton:
		var mouse_event := event as InputEventMouseButton
		if not mouse_event.pressed and current_item:
			use_item(current_item)


func set_current_item(item: Node):
	current_item = item


func use_item(item: Node) -> void:
	used_items.append(item)


func _on_item_used() -> void:
	var item = used_items.pop_front()
	if item != null:
		_use_item(item)
	else:
		_complete_run()

func _complete_run() -> void:
	print("used items: %s"%[used_items_names])
	yield(get_tree().create_timer(0.5), "timeout")
	Events.emit_signal("practice_run_completed")


func _use_item(item: Node) -> void:
	var index = item.get_index()
	# warning-ignore:unsafe_method_access
	var item_name = item.get_texture_name()
	print("using item %s: \"%s\""%[index, item_name])
	# warning-ignore:unsafe_method_access
	item.use()
	used_items_names.append(item_name)


func _run():
	pick_items()
	_on_item_used()


# EXPORT pick
var inventory = [
	"health",
	"ice",
	"lightning",
	"fire",
	"gem",
	"lightning",
	"health",
	"ice",
	"fire",
	"lightning",
	"fire",
	"health"
]

func pick_items():
	use_item(inventory[3])
	use_item(inventory[5])
# /EXPORT pick
