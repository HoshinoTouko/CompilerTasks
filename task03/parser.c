
/************************************************************/
/*      copyright hanfei.wang@gmail.com                     */
/*             2018.09.20                                   */
/************************************************************/

#include <ctype.h>
#include <stdlib.h>
#include "ast.h"

/* reg -> term  reg'
   reg' -> '|' term reg' | epsilon
   term -> kleene term'
   term' -> kleene term' | epsilon
   kleene -> fac kleene'
   kleene' -> * kleene' | epsilon
   fac -> alpha | '(' reg ')'
*/
static char input_buffer[MAX_STATES] = "\0";

static char * current = input_buffer;
/* our match - advance in XL parser is corresponding
   here (* current = ? ) - next_token() */


void next_token(void)
{
  if ( !*current ) {
    current = input_buffer;
    if ( !fgets(input_buffer, MAX_STATES - 1, stdin) ) {
      *current = '\0';
      return;
    }
  } else current ++;

  while ( isspace (*current) )
    current ++;
  //  printf("current char is %c\n", *current);
 }

AST_PTR reg();
AST_PTR reg1(AST_PTR term_left);
AST_PTR term ();
AST_PTR term1(AST_PTR kleene_left);
AST_PTR kleene();
AST_PTR kleene1( AST_PTR fac_left);
AST_PTR fac();
///**********************��˼���⡿ȥ���������ŵĺ���********************///
void simplify_print ( AST_PTR tree);


AST_PTR start()
{
  AST_PTR leaf, root = reg ();///main����ֻ������start����start��ֻ������reg��˵������֮����Ȼ��ѭ��������õĹ�ϵ
  pos ++;
  leaf = mkLeaf('$', 0);
  root = mkOpNode(Seq, root, leaf); //root��leaf�ֱ������Ӻ��Һ���
  simplify_print( root );///��ӡ���ʽ

  if ( *current != '\0' )
    printf("the parser finished at %c, before the end of RE\n", *current);
  return root;
}

/* reg -> term  reg' */
AST_PTR reg()
{
  /* �����!!! */
  AST_PTR left;
  left = term();//����������
  return reg1(left);
}

/*  reg' -> '|' term reg' | epsilon */
AST_PTR reg1(AST_PTR term_left)
{
  /* �����!!! */

}

/*  term -> kleene term' */
AST_PTR term ()
{
  /* �����!!! */
}

/*  term' -> kleene term' | epsilon */
AST_PTR term1(AST_PTR kleene_left)
{
  /* �����!!! */
}

/*  kleene -> fac kleene' */
AST_PTR kleene()
{
  /* �����!!! */
}

/*   kleene' -> * kleene' | epsilon */
AST_PTR kleene1( AST_PTR fac_left)
{
  /* �����!!! */
}

/*   fac -> alpha | '(' reg ')' */
AST_PTR fac()
{
  /* �����!!! */
}


void simplify_print ( AST_PTR tree)
{
  /* �����(ѡ��)!!! */
}


