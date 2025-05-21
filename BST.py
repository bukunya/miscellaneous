class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert_recursive(node.right, value)

    def search(self, value):
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node, value):
        if node is None:
            return False

        if node.value == value:
            return True
        elif value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)

    def find_min(self):
        if self.root is None:
            return None

        current = self.root
        while current.left:
            current = current.left

        return current.value

    def find_max(self):
        if self.root is None:
            return None

        current = self.root
        while current.right:
            current = current.right

        return current.value

    def inorder_traversal(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)

    def preorder_traversal(self):
        result = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, node, result):
        if node:
            result.append(node.value)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)

    def postorder_traversal(self):
        result = []
        self._postorder_recursive(self.root, result)
        return result

    def _postorder_recursive(self, node, result):
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.value)

def test_bst():
    print("\n===== Mengetes Binary Search Tree =====")
    bst = BinarySearchTree()

    values = [50, 30, 70, 20, 40, 60, 80]
    print("Nilai yang dimasukkan:", values)
    for value in values:
        bst.insert(value)

    print(f"Mencari nilai 40: {bst.search(40)}")
    print(f"Mencari nilai 90: {bst.search(90)}")

    print(f"Nilai minimum: {bst.find_min()}")
    print(f"Nilai maksimum: {bst.find_max()}")

    print(f"Inorder traversal: {bst.inorder_traversal()}")
    print(f"Preorder traversal: {bst.preorder_traversal()}")
    print(f"Postorder traversal: {bst.postorder_traversal()}")

if __name__ == "__main__":
    test_bst()
