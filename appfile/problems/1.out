class Solution {
public:
    map<char,int> m;
    void init()
    {
        m['I'] = 1; m['V'] = 5; m['X'] = 10;
        m['L'] = 50; m['C'] = 100; m['D'] = 500;
        m['M'] = 1000;
    }
    int romanToInt(string s) {

        init();

        int len = s.size();
        int ans = 0, pre = 0;

        for(int i = len-1; i >= 0; i--)
        {
            if(m[s[i]] >= pre) ans += m[s[i]];
            else  ans -= m[s[i]];
            pre = m[s[i]];
        }

        return ans;
    }
};
