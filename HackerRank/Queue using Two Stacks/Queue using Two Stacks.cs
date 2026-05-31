using System;
using System.Collections.Generic;
using System.IO;
class Solution {
    static void Main(String[] args) {
        /* Enter your code here. Read input from STDIN. Print output to STDOUT. Your class should be named Solution */
        Stack<int> inputStack = new Stack<int>();
        Stack<int> outputStack = new Stack<int>();
        
        int queries = Convert.ToInt32(Console.ReadLine());
        
        for(int i=0;i<queries;i++){
            string[] query = Console.ReadLine().Split(" ");
            int type = Convert.ToInt32(query[0]);
            if(type == 1){
                //enqueue
                int element = int.Parse(query[1]);
                //push into stack
                inputStack.Push(element);
                
            }
            else if(type == 2){
                //dequeue
                    //copy all into the output stack
                    CopyStack(inputStack,outputStack);
                    //pop first element out from the output stack
                    outputStack.Pop();
            }
            else if(type ==3){
                //copy into the output stack
                CopyStack(inputStack,outputStack);
                //print the first element
                Console.WriteLine(outputStack.Peek());
            }
        }
    }
    
    static void CopyStack(Stack<int> inputStack, Stack<int> outputStack)
    {
        if(outputStack.Count == 0)
        {
            while(inputStack.Count > 0)
            {
                outputStack.Push(inputStack.Pop());
            }
        }
    }
    
    
}
