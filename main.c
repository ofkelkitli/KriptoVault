	#include <stdio.h>
	#include <stdlib.h>
	#include <string.h>
	#include <stdbool.h>
	#include <windows.h>
	
	#include "functions.h"
	#include "encrypter.h"
	#include "decrypter.h"
	
	char masterKey[100];
	char key1[50];
	char key2[50];
	
	bool girildiMi = false;
	
	FILE *passFILE;
	
	int main() {
		passFILE = fopen("password.bin", "rb");
		
		if(passFILE == NULL){
			printf(YESIL"-----SISTEM KURULUMU-----\n\n"RESET);
			
			printf(SARI"Ana Sifre Olusturun: "RESET);
			fgets(masterKey, sizeof(masterKey), stdin);
			masterKey[strcspn(masterKey, "\n")] = '\0';
			
			printf(TURKUAZ"\nIlk Keyi Giriniz: "RESET);
			fgets(key1, sizeof(key1), stdin);
			key1[strcspn(key1, "\n")] = '\0';
			
			printf(TURKUAZ"\nIkinci Keyi Giriniz: "RESET);
			fgets(key2, sizeof(key2), stdin);
			key2[strcspn(key2, "\n")] = '\0';
			
			int key1Lenght = strlen(key1);
			int key2Lenght = strlen(key2);
			int masterKeyLenght = strlen(masterKey);
			
			encrypt(masterKey, masterKeyLenght, key1, key2);
			encrypt(key1, key1Lenght, masterKey, key2);
			encrypt(key2, key2Lenght, key1, masterKey);
			
			passFILE = fopen("password.bin", "wb");
			
			if(passFILE != NULL){	
				fwrite(&key1Lenght, sizeof(int), 1, passFILE);
				fwrite(&key2Lenght, sizeof(int), 1, passFILE);
				fwrite(&masterKeyLenght, sizeof(int), 1, passFILE);
				
				fwrite(key1, sizeof(char), key1Lenght, passFILE);
				fwrite(key2, sizeof(char), key2Lenght, passFILE);
				fwrite(masterKey, sizeof(char), masterKeyLenght, passFILE);
				
				fclose(passFILE);
				printf(YESIL"\nKurulum Tamamlandi! Lutfen Programi Yeniden Baslatiniz!\n"RESET);
				return 0;
			}
		}
		else {
			int key1Lenght;
			int key2Lenght;
			int masterKeyLenght;
			
			fread(&key1Lenght, sizeof(int), 1, passFILE);
			fread(&key2Lenght, sizeof(int), 1, passFILE);
			fread(&masterKeyLenght, sizeof(int), 1, passFILE);
			
			fread(key1, sizeof(char), key1Lenght, passFILE);
			key1[key1Lenght] = '\0';
			
			fread(key2, sizeof(char), key2Lenght, passFILE);
			key2[key2Lenght] = '\0';
			
			fread(masterKey, sizeof(char), masterKeyLenght, passFILE);
			masterKey[masterKeyLenght] = '\0';
			
			fclose(passFILE);
			
			char yedekKey1[50];
			char yedekKey2[50];
			char yedekMasterKey[100];
			
			memcpy(yedekKey1, key1, sizeof(key1));
        	memcpy(yedekKey2, key2, sizeof(key2));
        	memcpy(yedekMasterKey, masterKey, sizeof(masterKey));
			
			do{
				memcpy(key1, yedekKey1, sizeof(key1));
            	memcpy(key2, yedekKey2, sizeof(key2));
            	memcpy(masterKey, yedekMasterKey, sizeof(masterKey));
				
				char girilenSifre[100];
				printf(SARI"Sifrenizi Giriniz: "RESET);
				fgets(girilenSifre, sizeof(girilenSifre), stdin);
				girilenSifre[strcspn(girilenSifre, "\n")] = '\0';
				
				decrypt(key2, key2Lenght, key1, masterKey);
				decrypt(key1, key1Lenght, masterKey, key2);
				encrypt(girilenSifre, strlen(girilenSifre), key1, key2);
				
				if(strlen(girilenSifre) == masterKeyLenght && memcmp(girilenSifre, masterKey, masterKeyLenght) == 0){
					printf(YESIL"\n>>Giris Basarili! Hosgeldin Omer Kingo!\n"RESET);
					girildiMi = true;
				}
				else{
					printf(KIRMIZI"\n>>Giris Basarisiz! Yeniden Deneyiniz!\n"RESET);
					girildiMi = false;
					return 1;
				}
			}while(!girildiMi);		
		}
		
		if(girildiMi){
			int secim = 0;
			
			do{
				printf(MAVI"\n---ANA MENU---\n"RESET);
				printf(TURKUAZ"1 * Sifreleri Listeleme\n"RESET);
				printf(TURKUAZ"2 * Sifre Ekleme\n"RESET);
				printf(TURKUAZ"3 * Sifre Guncelleme\n"RESET);
				printf(TURKUAZ"4 * Sifre Silme\n"RESET);
				printf(TURKUAZ"5 * Guclu Sifre Onerici\n"RESET);
				printf(TURKUAZ"9 * Cikis\n"RESET);
				printf(P_SARI"Seciminizi Giriniz: "RESET);
				char secimGirdisi[10];
				fgets(secimGirdisi, sizeof(secimGirdisi), stdin);
				if(secimGirdisi[0] == '\n'){
					system("cls");
					continue;
				}
				secim = atoi(secimGirdisi);
				printf("\n");
				
				switch(secim){
					case 1: {
						FILE *vault = fopen("vault.bin", "rb");
						if(vault == NULL){
							printf(KIRMIZI"\n>>Hicbir Sifre Eklenmemis!\n"RESET);
						}
						else{
							printf(MAVI"---KAYITLI SIFRELER---\n"RESET);
							int siteLenght;
							int usernameLenght;
							int passwordLenght;
							char siteName[50];
							char username[50];
							char password[50];
							
							while(fread(&siteLenght, sizeof(int), 1, vault) == 1){
								fread(siteName, sizeof(char), siteLenght, vault);
								decrypt(siteName, siteLenght, key1, key2);
								siteName[siteLenght] = '\0';
								
								fread(&usernameLenght, sizeof(int), 1, vault);
								fread(username, sizeof(char), usernameLenght, vault);
								decrypt(username, usernameLenght, key1, key2);
								username[usernameLenght] = '\0';
								
								fread(&passwordLenght, sizeof(int), 1, vault);
								fread(password, sizeof(char), passwordLenght, vault);
								decrypt(password, passwordLenght, key1, key2);
								password[passwordLenght] = '\0';
								
								printf(TURKUAZ"Platform: "P_TURKUAZ"%s"P_GRI" | "TURKUAZ"Kullanici Adi: "P_TURKUAZ"%s"P_GRI" | "TURKUAZ"Sifre: "P_TURKUAZ"%s\n"RESET, siteName, username, password);
							}
							fclose(vault);
						}
						break;
					}
					
					case 2: {
						char site[50];
						char username[50];
						char password[50];
						
						printf(MAVI"---EKLEME MENUSU---\n\n"RESET);
						printf(TURKUAZ"Platform'u giriniz(9 ile cikis yapilir): "RESET);
						fgets(site, sizeof(site), stdin);
						site[strcspn(site, "\n")] = '\0';
						
						if(strcmp(site, "9") == 0){
							printf(KIRMIZI"\n>>Sistemden Cikis Yapiliyor!"RESET);
							break;
						}
						
						printf(TURKUAZ"Kullanici Adini Giriniz(9 ile cikis yapilir): "RESET);
						fgets(username, sizeof(username), stdin);
						username[strcspn(username, "\n")] = '\0';
						
						if(strcmp(username, "9") == 0){
							printf(KIRMIZI"\n>>Sistemden Cikis Yapiliyor!"RESET);
							break;
						}
						
						printf(TURKUAZ"Sifreyi Giriniz(9 ile cikis yapilir): "RESET);
						fgets(password, sizeof(password), stdin);
						password[strcspn(password, "\n")] = '\0';
						
						if(strcmp(password, "9") == 0){
							printf(KIRMIZI"\n>>Sistemden Cikis Yapiliyor!"RESET);
							break;
						}
						
						int siteLenght = strlen(site);
						int usernameLenght = strlen(username);
						int passwordLenght = strlen(password);
						
						if(siteLenght == 0 || usernameLenght == 0 || passwordLenght == 0){
							printf(KIRMIZI"\n>>Bilgiler Bos Birakilamaz!\n"RESET);
							break;
						}
						
						encrypt(site, siteLenght, key1, key2);
						encrypt(username, usernameLenght, key1, key2);
						encrypt(password, passwordLenght, key1, key2);
						
						FILE *vault = fopen("vault.bin", "ab");
						if(vault != NULL){
							fwrite(&siteLenght, sizeof(int), 1, vault);
							fwrite(site, sizeof(char), siteLenght, vault);
							
							fwrite(&usernameLenght, sizeof(int), 1, vault);
							fwrite(username, sizeof(char), usernameLenght, vault);
							
							fwrite(&passwordLenght, sizeof(int), 1, vault);
							fwrite(password, sizeof(char), passwordLenght, vault);
							
							fclose(vault);
							printf(YESIL">>Sifre Basariyla Kaydedildi!\n"RESET);
						}
						break;
					}
						
					case 3: {
						FILE *vault = fopen("vault.bin", "rb");
						if(vault== NULL){
							printf(KIRMIZI"\n>>Hicbir Sifre Eklenmemis!\n"RESET);
							break;
						}
						
						printf(MAVI"---GUNCELLEME MENUSU---\n"RESET);
						
						int siteLenght;
						int usernameLenght;
						int passwordLenght;
						
						char site[50];
						char username[50];
						char password[50];
						
						int sayac = 1;
						
						while(fread(&siteLenght, sizeof(int), 1, vault) == 1){
							fread(site, sizeof(char), siteLenght, vault);
							decrypt(site, siteLenght, key1, key2);
							site[siteLenght] = '\0';
							
							fread(&usernameLenght, sizeof(int), 1, vault);
							fread(username, sizeof(char), usernameLenght, vault);
							decrypt(username, usernameLenght, key1, key2);
							username[usernameLenght] = '\0';
							
							fread(&passwordLenght, sizeof(int), 1, vault);
							fread(password, sizeof(char), passwordLenght, vault);
							
							printf(MOR"%d"P_GRI" -"TURKUAZ" Platform: "P_TURKUAZ"%s "P_GRI"| "TURKUAZ"Kullanici Adi: "P_TURKUAZ"%s\n"RESET, sayac, site, username);
							sayac++;
						}
						
						if(sayac == 1){
							printf(KIRMIZI"\n>>Sistemde Kayitli Sifre Bulunamadi!\n"RESET);
							fclose(vault);
							break;
						}
						
						int guncellenecekNumara = 0;
						printf(TURKUAZ"Guncellenecek Numarayi Giriniz(9 ile cikis yapilir): "RESET);
						char guncelGirdi[10];
						fgets(guncelGirdi, sizeof(guncelGirdi), stdin);
						
						if(guncelGirdi[0] == '\n'){
							printf(KIRMIZI"\n>>Islem iptal edildi (Bos giris yaptiniz)!\n"RESET);
							fclose(vault);
							break;
						}
						
						guncellenecekNumara = atoi(guncelGirdi);
						
						if(guncellenecekNumara == 9){
							printf(KIRMIZI"\n>>Sistemden Cikis Yapiliyor!\n"RESET);
							fclose(vault);
							break;
						}
						
						FILE *temp = fopen("temp.bin", "wb");
						
						if(temp == NULL){
							printf(KIRMIZI"\n>>Gecici Dosya Olusturulamadi!\n"RESET);
							fclose(vault);
							break;
						}
						
						rewind(vault);
						
						sayac = 1;
						bool guncellendiMi = false;
						
						while(fread(&siteLenght, sizeof(int), 1, vault)){
							fread(site, sizeof(char), siteLenght, vault);
							site[siteLenght] = '\0';
							
							fread(&usernameLenght, sizeof(int), 1, vault);
							fread(username, sizeof(char), usernameLenght, vault);
							
							fread(&passwordLenght, sizeof(int), 1, vault);
							fread(password, sizeof(char), passwordLenght, vault);
							
							if(sayac != guncellenecekNumara){
								fwrite(&siteLenght, sizeof(int), 1, temp);
								fwrite(site, sizeof(char), siteLenght, temp);
								
								fwrite(&usernameLenght, sizeof(int), 1, temp);
								fwrite(username, sizeof(char), usernameLenght, temp);
								
								fwrite(&passwordLenght, sizeof(int), 1, temp);
								fwrite(password, sizeof(char), passwordLenght, temp);
							}
							else {
								guncellendiMi = true;
								
								char yeniUsername[50];
								char yeniPassword[50];
								
								decrypt(site, siteLenght, key1, key2);
								printf(TURKUAZ"\n>>%s "YESIL"Platformu Icin Degisiklikler Yapiliyor!\n"RESET, site);
								
								printf(TURKUAZ"Yeni Kullanici Adini Giriniz: "RESET);
								fgets(yeniUsername, sizeof(yeniUsername), stdin);
								yeniUsername[strcspn(yeniUsername, "\n")] = '\0';
								
								printf(TURKUAZ"Yeni Sifreyi Giriniz: "RESET);
								fgets(yeniPassword, sizeof(yeniPassword), stdin);
								yeniPassword[strcspn(yeniPassword, "\n")] = '\0';
								
								int yeniUsernameLenght = strlen(yeniUsername);
								int yeniPasswordLenght = strlen(yeniPassword);
								
								encrypt(site, siteLenght, key1, key2);
								encrypt(yeniUsername, yeniUsernameLenght, key1, key2);
								encrypt(yeniPassword, yeniPasswordLenght, key1, key2);
								
								fwrite(&siteLenght, sizeof(int), 1, temp);
								fwrite(site, sizeof(char), siteLenght, temp);
								
								fwrite(&yeniUsernameLenght, sizeof(int), 1, temp);
								fwrite(yeniUsername, sizeof(char), yeniUsernameLenght, temp);
								
								fwrite(&yeniPasswordLenght, sizeof(int), 1, temp);
								fwrite(yeniPassword, sizeof(char), yeniPasswordLenght, temp);
							}
							sayac++;
						}
						
						fclose(vault);
						fclose(temp);
						
						if(guncellendiMi){
							remove("vault.bin");
							rename("temp.bin", "vault.bin");
							printf(YESIL">>%d Numarali Dosya Basariyla Guncellendi!\n"RESET, guncellenecekNumara);
						}
						else {
							remove("temp.bin");
							printf(KIRMIZI">>Gecersiz Numara Girdiniz!\n"RESET);
						}
							
						break;
					}
						
					case 4:{
						FILE *vault = fopen("vault.bin", "rb");
						if(vault == NULL){
							printf(KIRMIZI"\n>>Hicbir Sifre Eklenmemis!\n"RESET);
							break;
						}
						
						printf(MAVI"---SILME MENUSU---\n"RESET);
						int siteLenght;
						int usernameLenght;
						int passwordLenght;
						
						char site[50];
						char username[50];
						char password[50];
						
						int sayac = 1;
						
						while(fread(&siteLenght, sizeof(int), 1, vault) == 1){
							fread(site, sizeof(char), siteLenght, vault);
							decrypt(site, siteLenght, key1, key2);
							site[siteLenght] = '\0';
							
							fread(&usernameLenght, sizeof(int), 1, vault);
							fread(username, sizeof(char), usernameLenght, vault);
							decrypt(username, usernameLenght, key1, key2);
							username[usernameLenght] = '\0';
							
							fread(&passwordLenght, sizeof(int), 1, vault);
							fread(password, sizeof(char), passwordLenght, vault);
							
							printf(MOR"%d"P_GRI" - "TURKUAZ"Platform: "P_TURKUAZ"%s "P_GRI"| "TURKUAZ"Kullanici Adi: "P_TURKUAZ"%s\n"RESET, sayac, site, username);
							sayac++;
						}
						
						if(sayac == 1){
							printf(KIRMIZI"\n>>Sistemde Kayitli Sifre Bulunamadi!\n"RESET);
							fclose(vault);
							break;
						}
						
						int silinecekNumara = 0;
						printf(TURKUAZ"Silmek Istediginiz Sira Numarasini Giriniz(9 ile cikis yapilir): "RESET);
						char silmeGirdi[10];
						fgets(silmeGirdi, sizeof(silmeGirdi), stdin);
						
						if(silmeGirdi[0] == '\n'){
							printf(KIRMIZI"\n>>Islem iptal edildi (Bos giris yaptiniz)!\n"RESET);
							fclose(vault);
							break;
						}
						
						silinecekNumara = atoi(silmeGirdi);
						
						if(silinecekNumara == 9){
							printf(KIRMIZI"\n>>Sistemden Cikis Yapiliyor!"RESET);
							fclose(vault);
							break;
						}
						
						FILE *temp = fopen("temp.bin", "wb");
						if(temp == NULL){
							printf(KIRMIZI">>Gecici Dosya Olusturulamadi!\n"RESET);
							fclose(vault);
							break;
						}
						
						rewind(vault);
						
						sayac = 1;
						bool silindiMi = false;
						
						while(fread(&siteLenght, sizeof(int), 1, vault) == 1){
							fread(site, sizeof(char), siteLenght, vault);
							
							fread(&usernameLenght, sizeof(int), 1, vault);
							fread(username, sizeof(char), usernameLenght, vault);
							
							fread(&passwordLenght, sizeof(int), 1, vault);
							fread(password, sizeof(char), passwordLenght, vault);
							
							if(sayac != silinecekNumara){
								fwrite(&siteLenght, sizeof(int), 1, temp);
								fwrite(site, sizeof(char), siteLenght, temp);
								
								fwrite(&usernameLenght, sizeof(int), 1, temp);
								fwrite(username, sizeof(char), usernameLenght, temp);
								
								fwrite(&passwordLenght, sizeof(int), 1, temp);
								fwrite(password, sizeof(char), passwordLenght, temp);
							}
							else {
								silindiMi = true;
							}
							sayac++;
						}
						
						fclose(vault);
						fclose(temp);
						
						if(silindiMi){
							remove("vault.bin");
							rename("temp.bin", "vault.bin");
							printf(YESIL">>%d Numarali Dosya Basariyla Silindi!\n"RESET, silinecekNumara);
						}
						else {
							remove("temp.bin");
							printf(KIRMIZI">>Gecersiz Numara Girdiniz!\n"RESET);
						}
						
						break;
					}
					
					case 5: {
						int uzunluk = 0;
						char sifre[100];
						
						printf(TURKUAZ"Olusturulacak Sifre Kac Karakterli Olsun: "RESET);
						char uzunlukGirdisi[10];
						fgets(uzunlukGirdisi, sizeof(uzunlukGirdisi), stdin);
						
						if(uzunlukGirdisi[0] == '\n'){
							printf(KIRMIZI"\n>>Islem iptal edildi (Bos giris yaptiniz)!\n"RESET);
							break;
						}
						
						uzunluk = atoi(uzunlukGirdisi);
						
						if(uzunluk > 0 && uzunluk <= 99){
							srand((unsigned int)GetTickCount());
							char karakterHavuzu[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?";
							int havuzBoyutu = strlen(karakterHavuzu);
							
							for(int i = 0; i<uzunluk; i++){
								int rastgeleIndex = rand() % havuzBoyutu;
								sifre[i] = karakterHavuzu[rastgeleIndex];
							}
							sifre[uzunluk] = '\0';
							
							printf(YESIL"\nUretilen Guclu Sifreniz: "P_TURKUAZ"%s\n"RESET, sifre);
						}
						else {
							printf(KIRMIZI"\n>>Gecersiz Uzunluk! Lutfen 1 ile 99 Arasinda Bir Deger Giriniz!\n"RESET);
							break;
						}
						break;
					}
								
					case 9:
						break;
											
					default:
						printf(KIRMIZI">>Lutfen Gecerli Secim Yapiniz!\n"RESET);
						break;
					
				}
				
				if(secim != 9){
					printf(SARI"\nDevam Etmek Icin Enter'a Basin..."RESET);
					int c;
					while((c = getchar()) != '\n' && c != EOF){	}
					system("cls");	
				}
			}while(secim != 9);
		}
		
		memset(key1, 0, sizeof(key1));
		memset(key2, 0, sizeof(key2));
		memset(masterKey, 0, sizeof(masterKey));
		
		printf(KIRMIZI">>Sistemden Cikis Yapildi!\n"RESET);
		
		return 0;
	}
