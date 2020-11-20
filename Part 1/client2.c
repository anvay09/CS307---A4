#include <stdio.h> 
#include <sys/socket.h> 
#include <arpa/inet.h> 
#include <unistd.h> 
#include <string.h> 
#define PORT 8080 
   
char SERVER_IP[] = "10.0.2.15"; //VM 1 IP

int main(int argc, char const *argv[]) 
{ 
    int sock = 0, valread; 
    struct sockaddr_in serv_addr;  
    char buffer[1000] = {0}; 

    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) 
    { 
        printf("\n Socket creation error \n"); 
        return -1; 
    } 
   
    serv_addr.sin_family = AF_INET; 
    serv_addr.sin_port = htons(PORT); 
       
    if(inet_pton(AF_INET, SERVER_IP, &serv_addr.sin_addr)<=0)  
    { 
        printf("\nInvalid address/ Address not supported \n"); 
        return -1; 
    } 
   
    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) 
    { 
        printf("\nConnection Failed \n"); 
        return -1; 
    } 

    while (1)
    {
        char message[1000];
        printf("Enter String to be sent to server : ");
        scanf("%[^\n]%*c", message);

        send(sock, message, strlen(message), 0 ); 
        printf("String sent\n"); 
        valread = read(sock, buffer, 1000); 
        printf("Recieved string from server : %s\n", buffer); 

        printf("Continue (c) or quit (any other key) ? ");
        char A[2];
        scanf("%[^\n]%*c", A);
        if (A[0] == 'c') continue;
        else
        {
            char quitmessage[] = "<quit>"; 
            send(sock, quitmessage, strlen(quitmessage), 0);
            break;
        }
    }
    
    return 0; 
} 
