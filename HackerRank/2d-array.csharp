using System.CodeDom.Compiler;
using System.Collections.Generic;
using System.Collections;
using System.ComponentModel;
using System.Diagnostics.CodeAnalysis;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.Serialization;
using System.Text.RegularExpressions;
using System.Text;
using System;

class Result
{

    /*
     * Complete the 'hourglassSum' function below.
     *
     * The function is expected to return an INTEGER.
     * The function accepts 2D_INTEGER_ARRAY arr as parameter.
     */

    public static int hourglassSum(List<List<int>> arr)
    {
        // 2. Initialize the 2D array with those dimensions
        //int[,] matrix2D = new int[6, 6];
        
        int[] toprow = new int[16];
        int[] middlerow = new int[16];
        int[] bottomrow= new int[16];
        // 3. Copy the data over using nested loops
        int a=0;
        int max=int.MinValue;
        for (int i = 0; i < 4; i++)
        {
            for (int j = 0; j < 4; j++)
            {
                
                toprow[a]=arr[i][j]+arr[i][j+1]+arr[i][j+2];
                middlerow[a]=arr[i+1][j+1];
                bottomrow[a]=arr[i+2][j]+arr[i+2][j+1]+arr[i+2][j+2];

                int sum = toprow[a]+middlerow[a]+bottomrow[a];
                if(sum > max){
                    max = sum;
                }
                a++;
            }
        }
        return max;
    }

}

class Solution
{
    public static void Main(string[] args)
    {
        TextWriter textWriter = new StreamWriter(@System.Environment.GetEnvironmentVariable("OUTPUT_PATH"), true);

        List<List<int>> arr = new List<List<int>>();

        for (int i = 0; i < 6; i++)
        {
            arr.Add(Console.ReadLine().TrimEnd().Split(' ').ToList().Select(arrTemp => Convert.ToInt32(arrTemp)).ToList());
        }

        int result = Result.hourglassSum(arr);

        textWriter.WriteLine(result);

        textWriter.Flush();
        textWriter.Close();
    }
}
