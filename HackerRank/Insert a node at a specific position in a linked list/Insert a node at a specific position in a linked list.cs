
	/*
     * Complete the 'insertNodeAtPosition' function below.
     *
     * The function is expected to return an INTEGER_SINGLY_LINKED_LIST.
     * The function accepts following parameters:
     *  1. INTEGER_SINGLY_LINKED_LIST llist
     *  2. INTEGER data
     *  3. INTEGER position
     */

    /*
     * For your reference:
     *
     * SinglyLinkedListNode
     * {
     *     int data;
     *     SinglyLinkedListNode next;
     * }
     *
     */

    static SinglyLinkedListNode insertNodeAtPosition(SinglyLinkedListNode llist, int data, int position)
    {
		// Returns the input list without modification; actual logic to be implemented here.
        SinglyLinkedListNode newNode = new SinglyLinkedListNode(data);
        SinglyLinkedListNode current = llist;
        for(int i=1;i<position;i++){
            current = current.next;    
        }
        newNode.next = current.next;
        current.next = newNode;
		return llist;
    }

