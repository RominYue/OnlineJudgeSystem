class Solution {
public:
    int threeSumClosest(vector<int> &num, int target) {

        int ans = 1e9 +7,flag = 1;

        sort(num.begin(),num.end());

        int len = num.size();
        for(int i = 0; i < len - 2; i++)
        {
            for(int j = i + 1, k = len - 1; j < k;)
            {
                int tmp = num[j] + num[k] + num[i];
                if(tmp < target)
                {
                    if(target - tmp < ans)
                    {
                        ans = target - tmp;
                        flag = -1;
                    }
                    j++;
                }
                else
                {
                    if(tmp - target < ans)
                    {
                        ans = tmp - target;
                        flag = 1;
                    }
                    k--;
                }
            }
        }
        return target + flag*ans;
    }
};
