//simarjit.15976@lpu.co.in

/*
	Details are:
		1:Section Mentor.
		2:Section HOD.
		3:Course Coordinator.
		4:Placement Mentor.
		5:Class Representative.
		6:E-Cell Coordinator.
		7:Placement Coordinator.
*/
#include <iostream>
#include <cstring>
#include <fstream>
#include <conio.h>
#include <cstring>
using namespace std;
class AuthorityData
{
	long int regdno;
	// string name, autho, section;
	char name[30], autho[30], section[30];

public:
	void getData() //this member function is to get details
	{
		cout << "Registration Number :";
		cin >> regdno;
		cout << "Name :";
		fflush(stdin);
		cin.getline(name, 30);
		cout << "Authority Provided :";
		cin.getline(autho, 30);
		cout << "For the Section :";
		cin.getline(section, 30);
	}
	void showData() //this member function is to show details
	{
		cout << "\tRegistration Number :" << this->regdno << endl;
		cout << "\tName :" << this->name << endl;
		cout << "\tAuthority Provided :" << this->autho << endl;
		cout << "\tFor the Section :" << this->section << endl;
	}
	int returnRegdNo() //this member function is to return the registration number
	{
		return regdno;
	}
	char *returnSection() //this member fucntion is to return an character pointer of section which is also known as string (char array[])
	{
		return section;
	}
	char *returnAutho() //this member fucntion is to return an character pointer of autnority which is also known as string (char array[])
	{
		return autho;
	}
};
void showPartData()
{
	cout << "Enter from the Choice:" << endl;
	cout << "1.Section Mentor.\n2.Section HOD.\n3.Course Coordinator.\n4.Placement Mentor.\n5.Class Representative.\n6.E-Cell Coordinator.\n7.Placement Coordinator.\n";
	int choice;
	cin >> choice;
	AuthorityData ad;
	switch (choice)
	{
	case 1:
	{
		fstream lpu;
		lpu.open("LPUFinder.dat", ios::binary | ios::in);
		while (lpu.read((char *)&ad, sizeof(ad)))
		{
			if (strcmp(ad.returnAutho(), "Section Mentor") == 0)
			{
				ad.showData();
			}
		}
		lpu.close();
		break;
	}
	case 2:
	{
		fstream lpu;
		lpu.open("LPUFinder.dat", ios::binary | ios::in);
		while (lpu.read((char *)&ad, sizeof(ad)))
		{
			if (strcmp(ad.returnAutho(), "Section HOD") == 0)
			{
				ad.showData();
			}
		}
		lpu.close();
		break;
	}
	case 3:
	{
		fstream lpu;
		lpu.open("LPUFinder.dat", ios::binary | ios::in);
		while (lpu.read((char *)&ad, sizeof(ad)))
		{
			if (strcmp(ad.returnAutho(), "Course Coordinator") == 0)
			{
				ad.showData();
			}
		}
		lpu.close();
		break;
	}
	case 4:
	{
		fstream lpu;
		lpu.open("LPUFinder.dat", ios::binary | ios::in);
		while (lpu.read((char *)&ad, sizeof(ad)))
		{
			if (strcmp(ad.returnAutho(), "Placement Mentor") == 0)
			{
				ad.showData();
			}
		}
		lpu.close();
		break;
	}
	case 5:
	{
		fstream lpu;
		lpu.open("LPUFinder.dat", ios::binary | ios::in);
		while (lpu.read((char *)&ad, sizeof(ad)))
		{
			if (strcmp(ad.returnAutho(), "Class Representative") == 0)
			{
				ad.showData();
			}
		}
		lpu.close();
		break;
	}
	case 6:
	{
		fstream lpu;
		lpu.open("LPUFinder.dat", ios::binary | ios::in);
		while (lpu.read((char *)&ad, sizeof(ad)))
		{
			if (strcmp(ad.returnAutho(), "E-Cell Coordinator") == 0)
			{
				ad.showData();
			}
		}
		lpu.close();
		break;
	}
	case 7:
	{
		fstream lpu;
		lpu.open("LPUFinder.dat", ios::binary | ios::in);
		while (lpu.read((char *)&ad, sizeof(ad)))
		{
			if (strcmp(ad.returnAutho(), "Placement Coordinator") == 0)
			{
				ad.showData();
			}
		}
		lpu.close();
		break;
	}
	default:
		cout << "Entered The Wrong Choice." << endl;
	}
}
void showDatabase()
{
	fstream lpu;
	lpu.open("LPUFinder.dat", ios::binary | ios::in);
	if (lpu)
	{
		AuthorityData ad;
		cout << "******************** Database ********************\n";
		while (lpu.read((char *)&ad, sizeof(ad)))
		{
			ad.showData();
		}
		lpu.close();
	}
	else
	{
		cout << "File was empty." << endl;
	}
}
void sectionDetail()
{
	ifstream lpu;
	lpu.open("LPUFinder.dat", ios::binary);
	if (lpu)
	{
		AuthorityData ad;
		cout << "Enter the Section:";
		string sec;
		cin >> sec;
		bool f = 0;
		while (lpu.read((char *)&ad, sizeof(ad)))
		{
			if (sec.compare(ad.returnSection()) == 0)
			{
				f = 1;
				ad.showData();
			}
		}
		if (f == 0)
		{
			cout << "Data was not available." << endl;
		}
		lpu.close();
	}
	else
	{
		cout << "File was empty." << endl;
	}
}
void authorityDetail()
{
	ifstream lpu;
	lpu.open("LPUFinder.dat", ios::binary);
	if (lpu)
	{
		AuthorityData ad;
		long int regd;
		cout << "Enter the Registration Number of the higher authority:";
		cin >> regd;
		bool f = 0;
		while (lpu.read((char *)&ad, sizeof(ad)))
		{
			if (ad.returnRegdNo() == regd)
			{
				f = 1;
				ad.showData();
			}
		}
		if (f == 0)
		{
			cout << "Data was not available." << endl;
		}
		lpu.close();
	}
	else
	{
		cout << "File was empty." << endl;
	}
}
int accessing()
{
	system("cls");
	cout << "\t\t\t******************** LOGIN PAGE ********************\n";
	char *pass = new char[32];
	cout << "Enter the Password:";
	char a;
	int i = 0;
	while (true)
	{
		a = getch();
		if ((a >= 65 && a <= 90) || (a >= 97 && a <= 122) || (a >= 48 && a <= 57) || (a >= 33 && a <= 47) || (a >= 57 && a <= 64))
		{
			cout << "*";
			pass[i] = a;
			i++;
		}
		else if (a == '\b')
		{
			cout << "\b \b";
			i--;
		}
		else if (a == '\r')
		{
			pass[i] = '\0';
			break;
		}
		else
		{
			break;
		}
	}
	char password[] = "Adarsh2001";
	if (strcmp(pass, password) == 0 && strlen(pass) >= 6)
	{
		cout << "\n\tNow you will allowed to enter data:" << endl;
		cout << "Press any key to continue..." << endl;
		getch();
		return 1;
	}
	else
	{
		return 0;
	}
}
int main()
{
	int choice;
	do
	{
	h1:
		system("cls");
		cout << "\t\t\t******************** LPU Finder ********************\n";
		cout << "\t1.Administration. (NOT ALLOWED FOR STUDENTS ONLY ADMINISTRATOR CAN HANDLE THIS) \n";
		cout << "\t2.Search about a particular section.\n";
		cout << "\t3.Search about particular detail of a section.\n";
		cout << "\t4.Search About Higher Authority.\n";
		cout << "\t5.Exit.\n\t";
		cin >> choice;
		switch (choice)
		{
		case 1:
		{
		h2:
			if (accessing() == 1)
			{
				int ch;
			h3:
				do
				{
					system("cls");
					cout << "\t\t\t********** Welcome to Administration Department. **********\n";
					cout << "\t1.Create New Database.\n";
					cout << "\t2.Add details about Higher Authority.\n";
					cout << "\t3.Edit Database.\n";
					cout << "\t4.Display Whole Database.\n";
					cout << "\t5.Search about a particular section.\n";
					cout << "\t6.Search About Higher Authority.\n";
					cout << "\t7.Search about Particular details of a section.\n";
					cout << "\t8.Delete Database.\n";
					cout << "\t9.Go Back to Menu.\n";
					cin >> ch;
					switch (ch)
					{
					case 1:
					{
						char c;
						cout << "You are going to create a new Database. Are you sure? (Y/N):";
						cin >> c;
						if (c == 'Y' || c == 'y')
						{
							ofstream lpu;
							AuthorityData ad;
							char choice1;
							lpu.open("LPUFinder.dat", ios::binary | ios::out);
							do
							{
								ad.getData();
								lpu.write((char *)&ad, sizeof(ad));
								cout << "Want to enter more? (Y/N): ";
								cin >> choice1;
							} while (choice1 == 'y' || choice1 == 'Y');
							lpu.close();
						}
						else
						{
							goto h3;
						}
						break;
					}
					case 2:
					{
						fstream lpu;
						AuthorityData ad;
						lpu.open("LPUFinder.dat", ios::binary | ios::app);
						char choice1 = 'y';
						do
						{
							ad.getData();
							lpu.write((char *)&ad, sizeof(ad));
							cout << "Want to enter more? (Y/N): ";
							cin >> choice1;
						} while (choice1 == 'y' || choice1 == 'Y');
						lpu.close();
						break;
					}
					case 3:
					{
						fstream lpu;
						AuthorityData ad;
						lpu.open("LPUFinder.dat", ios::binary | ios::in | ios::out);
						cout << "Enter the Registration Number whose data want to change:";
						long int regd;
						cin >> regd;
						bool c = 0;
						while (!lpu.eof())
						{
							int pos = lpu.tellg();
							lpu.read((char *)&ad, sizeof(ad));
							if (ad.returnRegdNo() == regd && lpu)
							{
								c = 1;
								AuthorityData ad1;
								cout << "Enter the Revised Data for the same:" << endl;
								ad1.getData();
								lpu.seekp(pos, ios::beg);
								lpu.write((char *)&ad1, sizeof(ad1));
							}
						}
						if (c == 0)
						{
							cout << "You enter wrong Registration Number.\n";
						}
						lpu.close();
						break;
					}
					case 4:
					{
						showDatabase();
						cout << "Press any key to continue..." << endl;
						getch();
						break;
					}
					case 5:
					{
						sectionDetail();
						cout << "Press any key to continue..." << endl;
						getch();
						break;
					}
					case 6:
					{
						authorityDetail();
						cout << "Press any key to continue..." << endl;
						getch();
						break;
					}
					case 7:
					{
						showPartData();
						cout << "Press any key to continue..." << endl;
						break;
					}
					case 8:
					{
						fstream lpu, temp;
						lpu.open("LPUFinder.dat", ios::binary | ios::in);
						temp.open("temp.dat", ios::binary | ios::app | ios::out);
						AuthorityData ad;
						long int regd;
						int f = 0;
						cout << "Enter the Registration number of the Person:";
						cin >> regd;
						char choice;
						while (lpu.read((char *)&ad, sizeof(ad)))
						{
							if (ad.returnRegdNo() == regd)
							{
								f = 1;
								cout << "Are you sure? (Y/N)";
								cin >> choice;
								if (choice == 'N' || choice == 'n')
								{
									temp.write((char *)&ad, sizeof(ad));
								}
							}
							else
							{
								temp.write((char *)&ad, sizeof(ad));
							}
						}
						if (f == 0)
						{
							cout << "Content was not available." << endl;
						}
						else
						{
							lpu.close();
							temp.close();
							remove("LPUFinder.dat");
							rename("temp.dat", "LPUFinder.dat");
							remove("temp.dat");
							cout << "Content Deleted.\n";
							cout << "Want to see the Remaining Contents? (Y/N)";
							cin >> choice;
							if (choice == 'y' || choice == 'Y')
							{
								showDatabase();
								cout << "Press any key to continue..." << endl;
								getch();
							}
							else
							{
								goto h3;
							}
						}

						break;
					}
					case 9:
					{
						goto h1;
					}
					default:
					{
						cout << "You enter wrong choice." << endl;
					}
					}
				} while (true);
			}
			else
			{
				cout << "\n\tRe-enter the Password." << endl;
				cout << "Press any key to continue..." << endl;
				getch();
				goto h2;
			}
			break;
		}
		case 2:
		{
			sectionDetail();
			cout << "Press any key to continue..." << endl;
			getch();
			break;
		}
		case 3:
		{
			authorityDetail();
			cout << "Press any key to continue..." << endl;
			getch();
			break;
		}
		case 4:
		{
			exit(0);
			break;
		}
		default:
		{
			cout << "You enter wrong choice.\n";
		}
		}
	} while (true);
	return 0;
}
