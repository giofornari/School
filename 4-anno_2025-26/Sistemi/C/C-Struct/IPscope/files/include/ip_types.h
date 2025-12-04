#ifndef IP_TYPES_H
#define IP_TYPES_H

#include <stdint.h>
#include <stdbool.h>


typedef enum {
    IP_RESERVED,
    IP_PRIVATE,
    IP_PUBLIC
} IPType;



typedef struct {
    uint32_t ip_num;              
    char ip_str[16];              
    uint8_t octets[4];            
    
    uint32_t netmask;             
    uint8_t cidr_prefix;          
    uint32_t network_addr;        
    uint32_t broadcast_addr;      
    
    char class;                   
    IPType type;                  
    
    bool is_valid;                
} IPAddress;


typedef struct {
    int count;
    char class_filter;
    bool has_cidr;
    uint32_t cidr_network;
    uint8_t cidr_prefix;
    bool has_range;
    uint32_t range_start;
    uint32_t range_end;
} ProgramOptions;

#endif // IP_TYPES_H
