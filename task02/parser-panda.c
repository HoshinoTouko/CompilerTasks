
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

FOLLOW_INDEX cindex[MAX_STATES] = {0};
/*  pos index to the corresponding character and
    follow set, for dfa transformation only */

static char * current = input_buffer;
/* our match - advance in XL parser is corresponding
   here (* current = ? ) - next_token() */

static int pos = 0; /* for dfa only */


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
  //printf("current char is %c\n", *current);
 }

AST_PTR reg();
AST_PTR reg1(AST_PTR term_left);
AST_PTR term ();
AST_PTR term1(AST_PTR kleene_left);
AST_PTR kleene();
AST_PTR kleene1( AST_PTR fac_left);
AST_PTR fac();
///**********************【思考题】去掉多余括号的函数********************///
void simplify_print ( AST_PTR tree);


AST_PTR start()
{
  AST_PTR leaf, root = reg ();///main函数只调用了start，而start中只调用了reg，说明函数之间依然是循环互相调用的关系
  pos ++;
  leaf = mkLeaf('$', pos);
  root = mkOpNode(Seq, root, leaf); //root和leaf分别是左孩子和右孩子
  simplify_print( root );///打印最简式

  if ( *current != '\0' )
    printf("the parser finished at %c, before the end of RE\n", *current);
  return root;
}

/* reg -> term  reg' */
AST_PTR reg()
{
  /* 请完成!!! */
  //printf("reg: %c\n", *current);
  AST_PTR left;
  left = term();//生成左子树
  return reg1(left);
}

/*  reg' -> '|' term reg' | epsilon */
AST_PTR reg1(AST_PTR term_left)
{
  /* 请完成!!! */
  //printf("reg': %c\n", *current);
  char c = *current;
  if ( c == '|' ) {
    next_token();
    AST_PTR term_right;
    term_right = term();
    AST_PTR node = mkOpNode(Or, term_left, term_right);
    return reg1(node);
  }
  else
    return term_left;
}

/*  term -> kleene term' */
AST_PTR term ()
{
  /* 请完成!!! */
  //printf("term: %c\n", *current);
  AST_PTR left;
  left = kleene();
  return term1(left);
}

/*  term' -> kleene term' | epsilon */
AST_PTR term1(AST_PTR kleene_left)
{
  /* 请完成!!! */
  //printf("term': %c\n", *current);
  char c = *current;
  if ( isalpha(c) || isalnum(c) ) {
    AST_PTR kleene_right;
    kleene_right = kleene();
    AST_PTR node = mkOpNode(Seq, kleene_left, kleene_right);
    return term1(node);
  }
  else
    return kleene_left;
}

/*  kleene -> fac kleene' */
AST_PTR kleene()
{
  /* 请完成!!! */
  //printf("kleene: %c\n", *current);
  AST_PTR left;
  left = fac();
  return kleene1(left);
}

/*   kleene' -> * kleene' | epsilon */
AST_PTR kleene1( AST_PTR fac_left)
{
  /* 请完成!!! */
  //printf("kleene': %c\n", *current);
  char c = *current;
  if ( c == '*' ) { 
    next_token();
    AST_PTR right = mkEpsilon();
    AST_PTR node = mkOpNode(Star, fac_left, right);
    return node;
  }
  else
    return fac_left;
}

/*   fac -> alpha | '(' reg ')' */
AST_PTR fac()
{
  /* 请完成!!! */
  //printf("fac: %c\n", *current);
  char c = *current;
  if ( c == '(' ) {
    //printf("match (\n");
    next_token();
    AST_PTR node = reg();
    if ( (c=*current) == ')' ) {
      next_token();
      return node;
    }
    else {
      printf("no )\n");
      return node;
    }
  }
  else if ( isalpha(c) || isalnum(c) ) {
    //printf("match alpha\n");
    AST_PTR node = mkLeaf(c, pos);
    next_token();
    return node;
  }
  else {
    AST_PTR node = mkEpsilon();
    return node;
  }
}



void simplify_print ( AST_PTR tree)
{
  /* 请完成(选做)!!! */
  if ( tree==NULL ) {
    printf("attempt print empty tree!\n");
    return;
  }
  switch( tree->op ) {
    case Or:
      simplify_print( tree->lchild );
      printf("|");
      simplify_print( tree->rchild );
      return;
    case Seq:
      if ( ((tree->lchild)->op) < Seq ) {
        printf("(");
        simplify_print( tree->lchild );
        printf(")");
      }
      else
        simplify_print( tree->lchild );
      if ( ((tree->rchild)->op) < Seq ) {
        printf("(");
        simplify_print( tree->rchild );
        printf(")");
      }
      else
        simplify_print( tree->rchild );
      return;
    case Star:
      if ( ((tree->lchild)->op) < Star ) {
        printf("(");
        simplify_print( tree->lchild );
        printf(")");
        printf("*");
      }
      else
        simplify_print( tree->lchild );
        printf("*");
      return;
    case Alpha : 
      printf("%c", tree -> val);
      if ( tree->val == '$' )
        printf("\n");
      return;
    case Epsilon :
      printf("!");
      return;
  }
}


