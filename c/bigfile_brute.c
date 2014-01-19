#include <stdio.h>
#include <string.h>

// Clean removes the quotes and newlines.
void clean(char *cl, char *s) 
{
  char *word;
  char *sepchars = "\"\n";

  word = strtok(s, sepchars);
  while (word != NULL) {
	strcat(cl, word);
	  word = strtok(NULL, sepchars);
  }
}

// settings reads the Pythons settings.py file
// and searches for the key k.  If found it
// returns the value of the entry.  Otherwise,
// it returns NULL.
char *settings(char *s, char *k, char *value) {
  FILE *fp;
  if ((fp = fopen (s, "r" )) == NULL) {
	perror("Cannot open settings file.");
	//return NULL;
  }

  char line [256]; /* or other suitable maximum line size */
  char *word = NULL;
  //printf("settings: s=%s  k=%s\n", s,k);

  while ( fgets(line, sizeof line, fp ) != NULL ) {
	if ((strstr(line, k)) != NULL) {
	  if (line[0] == '#')
		continue;
	  word = strtok(line, " ");

	  int i;
	  for (i = 0; i <= 1; i++) {
		if ((word = strtok(NULL, " ")) == NULL) {
		  const char e[128] = {sprintf("settings: Couldn't find %s in %s\n.", k, s)};
		  perror(e);
		  return NULL;
		}
	  }
	  strcpy(value, word);
	  // printf("settings: Before return value=%s", value);
	  return value;
	}
  }
  return NULL;
}

int main (int argc, char *argv[])
{
  if(argc < 2) {
	printf("usage: bigfile_brute settings_file\n");
	return 1;
  }
  char *sfile = argv[1]; //settings file
  char buf[128] = {'\0'};
  char bigfile[128] = {"\0"};
  char query[128] = {'\0'};

  settings(sfile, "BIG_FILE", buf);
  clean(bigfile, buf);
  buf[0] = '\0';

  settings(sfile, "TARGET_USERNAME", buf);
  clean(query, buf);

   FILE *bfile = fopen (bigfile, "r" );
  if (bfile == NULL ) {
	perror (bigfile); // why didn't the file open? 
	return 1;
  }

  char line [256]; /* or other suitable maximum line size */
  char *q = "ssbrtg"; //TESTING ONLY
  //int recsread = 0;
  int recsmatch = 0;

  while(fgets(line, sizeof line, bfile) != NULL ) {
	//fputs ( line, stdout ); /* write the line */
	//recsread++;
	//Does line contain substring?
	if (strstr(line, query) != NULL) {
		recsmatch++;
	  }
  }
  fclose(bfile);
  //  printf("%d %d\n", recsread,recsmatch);
  printf("%d\n", recsmatch);
  return 0;
}
