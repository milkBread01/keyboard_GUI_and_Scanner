#include <iostream>
#include <vector>
#include <windows.h>
#include <cstdlib>
using std::cout;
using std::cin;
using std::endl;
using std::vector;
using std::string;


string detect_os(){
    #if defined(_WIN32)
        return "start ";
    #elif defined(__APPLE__)
        return "open ";
    #elif defined(__linux__)
        return "xdg-open ";
    #else
        return "";
    #endif
}

void open_link(string command_start, string website_link){
    website_link = command_start + website_link;
    system(website_link.c_str());
}

int main()
{
    string command_start = detect_os();
    if (command_start.empty()){
        cout<<"Unsopported Operating System"<<endl;
        return 1;
    }

    string website_link;
    cout<<"Enter link to website: ";
    cin>>website_link;
    open_link(command_start, website_link);


    return 0;
}