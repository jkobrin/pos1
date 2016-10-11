# -*- coding: UTF-8 -*-
import sys
import utils



#+---------------+------------+------+-----+---------------------+----------------+
#| Field         | Type       | Null | Key | Default             | Extra          |
#+---------------+------------+------+-----+---------------------+----------------+
#| id            | int(11)    | NO   | PRI | NULL                | auto_increment |
#| person_id     | int(4)     | YES  | UNI | NULL                |                |
#| married       | tinyint(1) | NO   |     | NULL                |                |
#| allowances    | int(11)    | NO   |     | 1                   |                |
#| nominal_scale | float      | NO   |     | 0                   |                |
#| created       | timestamp  | NO   |     | CURRENT_TIMESTAMP   |                |
#| updated       | timestamp  | NO   |     | 0000-00-00 00:00:00 |                |
#+---------------+------------+------+-----+---------------------+----------------+
#################################################################333
#
#   The following is an excerpt from:
#
#   Publication 15
#   Cat. No. 10000W(Circular E),
#   Employer's Tax Guide
#   http://www.irs.gov/pub/irs-pdf/p15.pdf#
#
#   It is used to calculate federal income tax withholding amounts
#
############################################################
#
#   Percentage Method Tables for Income Tax Withholding
#
#   (For Wages Paid in 2015)
#
#   TABLE 1—WEEKLY Payroll Period
#    
#    (a) SINGLE person (including head of household)—   
#    If the amount of wages  
#    (after subtracting  
#    withholding allowances) is:  The amount of income tax to withhold is:  
#    Not over $44                 $0     
#    Over—  But not over—                       of excess over— 
#    $44      —$222               $0.00 plus 10%      —$44      
#    $222     —$764               $17.80 plus 15%     —$222     
#    $764     —$1,789             $99.10 plus 25%     —$764     
#    $1,789   —$3,685             $355.35 plus 28%    —$1,789   
#    $3,685   —$7,958             $886.23 plus 33%    —$3,685   
#    $7,958   —$7,990             $2,296.32 plus 35%  —$7,958   
#    $7,990                       $2,307.52 plus 39.6%  —$7,990 
#
#(b) MARRIED person—  (including head of household)—   
#    If the amount of wages  
#    (after subtracting  
#    withholding allowances) is:  The amount of income tax to withhold is:  
#    Not over $165                 $0   
#    Over—   But not over—                   of excess over—
#    $165  —$520                   $0.00 plus 10%    —$165
#    $520  —$1,606                 $35.50 plus 15%   —$520
#    $1,606  —$3,073               $198.40 plus 25%  —$1,606
#    $3,073  —$4,597               $565.15 plus 28%  —$3,073
#    $4,597  —$8,079               $991.87 plus 33%  —$4,597
#    $8,079  —$9,105               $2,140.93 plus 35%—$8,079
#    $9,105                        $2,500.03 plus 39.6%                      
#    
##################################################################################

FEDERAL_WEEKLY_WITHHOLDING_ALLOWANCE = 76.90
SOCIAL_SECURITY_TAX_RATE = .062
MEDICARE_TAX_RATE = .0145

####################################################################################
#   The following are excerpts from:
#
#   http://www.tax.ny.gov/pdf/publications/withholding/nys50_t_nys.pdf
#
#
#   NYS-50-T-NYS (1/15)
#   New York State
#   Withholding Tax Tables
#   and Methods
#   Effective January 1, 2015
#
#   It is used to calculate New York state income tax withholding amounts
#
##############################################################################
#  Page 14 of 22  NYS-50-T-NYS (1/15)
#                                                                 New York State
#                                 Special Tables for Deduction and Exemption Allowances
#   Applicable to Method II, Exact Calculation Method                                                         Applicable to Dollar to Dollar Withholding Tables
#   for New York State; see pages 16 through 19                                                                      for New York State; see pages 20 and 21
#  
#  
#   Using the tables below, compute the total deduction and exemption allowance to subtract from wages.
#  
#  
#  Table A
#  Combined deduction and exemption allowance (full year)
#  
#  Using Payroll type, Marital status, and the Number of exemptions, locate the combined deduction and exemption allowance amount in
#  the chart below and subtract that amount from wages, before using the exact calculation method (or dollar to dollar withholding tables) to
#  determine the amount to be withheld.
#  
#  (Use Tables B and C below if more than 10 exemptions are claimed.)
#  
#                                                                                  Number of exemptions
#     Payroll      Marital
#      type        status        0          1            2         3           4           5             6             7           8           9          10
#  
#  Weekly          Single       141.35      160.60      179.85      199.10       218.35       237.60         256.85        276.10       295.35      314.60      333.85
#                  Married      150.95      170.20      189.45      208.70       227.95       247.20         266.45        285.70       304.95      324.20      343.45
#  
#################################################################333
#
#  Method II   Exact Calculation Method   New York State       SINGLE
#                                         Table II - A   Weekly Payroll         
#             If the amount of net                                                               
#             wages (after subtracting                                                           
#             deductions and                                                        Add the resul
#             exemptions) is:                           Subtract   Multiply the      to Column 5   
#                                                      Column 3     result by             amount.
#                                                                                                
#      L
#       i          At               But less          amount from    Column 4          Withhold the
#      n        Least                 than             net wages      amount         resulting sum
#      e         Column 1   Column 2                     Column 3     Column 4            Column 5  
#       1              $0              $162                     $0     0.0400                     $0 
#       2             162                223                   162     0.0450                   6.46 
#       3             223                264                   223     0.0525                   9.23 
#       4             264                407                   264     0.0590                  11.40 
#       5             407             1,531                    407     0.0645                  19.79 
#       6           1,531             1,838                  1,531     0.0665                  92.31 
#       7           1,838             2,042                  1,838     0.0758                 112.69 
#       8           2,042             3,064                  2,042     0.0808                 128.21 
#       9           3,064             4,087                  3,064     0.0715                 210.81 
#      10           4,087             5,108                  4,087     0.0815                 283.88 
#      11           5,108           20,436                   5,108     0.0735                 367.12 
#      12          20,436           21,459                  20,436     0.4902              1,493.71  
#      13          21,459   . . . . . . . . . .             21,459     0.0962              1,995.23  
#  
#  Method II   Exact Calculation Method   New York State       MARRIED
#  
#                                         Table II - A   Weekly Payroll                                
#             If the amount of net                                                                    
#             wages (after subtracting                                                                
#             deductions and                                                        Add the result    
#             exemptions) is:                           Subtract   Multiply the      to Column 5        
#                                                      Column 3     result by             amount.     
#                                                                                                     
#      L
#      i          At               But less          amount from    Column 4          Withhold the     
#      n        Least                 than             net wages      amount         resulting sum     
#      e          Column 1   Column 2                      Column 3     Column 4            Column 5     
#       1              $0              $162                     $0     0.0400                     $0      
#       2             162                223                   162     0.0450                   6.46      
#       3             223                264                   223     0.0525                   9.23      
#       4             264                407                   264     0.0590                  11.40      
#       5             407             1,531                    407     0.0645                  19.79      
#       6           1,531             1,838                  1,531     0.0665                  92.31      
#       7           1,838             2,042                  1,838     0.0728                 112.69      
#       8           2,042             3,064                  2,042     0.0778                 127.60      
#       9           3,064             4,087                  3,064     0.0808                 207.13      
#      10           4,087             6,130                  4,087     0.0715                 289.71      
#      11           6,130             7,152                  6,130     0.0815                 435.81      
#      12           7,152           20,436                   7,152     0.0735                 519.12      
#      13          20,436           40,874                  20,436     0.0765              1,495.46       
#      14          40,874           41,897                  40,874     0.8842              3,059.00       
#      15          41,897   . . . . . . . . . .             41,897     0.0962              3,963.60       
#############################################################################################################

# Data structure to represent on row of any of the above witholding tables (state, federal, single or married)
class TaxBracket(object):

  def __init__(self, bracket_start, base_withholding, pct_of_excess):
    self.bracket_start = bracket_start
    self.base_withholding = base_withholding
    self.pct_of_excess = pct_of_excess


# Based on the single federal table from Publication 15 in comments above
federal_single_withholding_table = (
  #bracket_start, base_withholding, pct_of_excess
  TaxBracket(44,    0.00,     10   ),
  TaxBracket(222,   17.80,    15   ),
  TaxBracket(764,   99.10,    25   ),
  TaxBracket(1789,  355.35,   28   ),
  TaxBracket(3685,  886.23,   33   ),
  TaxBracket(7958,  2296.32,  35   ),
  TaxBracket(7990,  2307.52,  39.6 ),
)

# Based on the married table from Publication 15 in comments above
federal_married_withholding_table = (
  #bracket_start, base_withholding, pct_of_excess
  TaxBracket(165, 0.00,      10  ),
  TaxBracket(520, 35.50,     15  ),
  TaxBracket(1606, 198.40,   25  ),
  TaxBracket(3073, 565.15,   28  ),
  TaxBracket(4597, 991.87,   33  ),
  TaxBracket(8079, 2140.93, 35  ),
  TaxBracket(9105, 2500.03,  39.6),
)


#  based on table from Page 14 of 22  NYS-50-T-NYS (1/15) excerpted above
single_nys_deductions_ordered_by_number_of_allowances= (
141.35,
160.60,
179.85,
199.10,
218.35,
237.60,
256.85,
276.10,
295.35,
314.60,
333.85)

#  based on table from Page 14 of 22  NYS-50-T-NYS (1/15) excerpted above
married_nys_deductions_ordered_by_number_of_allowances= (
150.95,
170.20,
189.45,
208.70,
227.95,
247.20,
266.45,
285.70,
304.95,
324.20,
343.45)


# Based on the single table from nys-50-t-nys in comments above
nys_single_withholding_table = (
  #bracket_start, base_withholding, pct_of_excess
  TaxBracket(0,    0,  0.0400),
  TaxBracket(162,  6.46,  0.0450),
  TaxBracket(223,  9.23,  0.0525),
  TaxBracket(264,  11.40,  0.0590),
  TaxBracket(407,  19.79,  0.0645),
  TaxBracket(1531, 92.31,  0.0665),
  TaxBracket(1838, 112.69,  0.0758),
  TaxBracket(2042, 128.21,  0.0808),
  TaxBracket(3064, 210.81,  0.0715),
  TaxBracket(4087, 283.88,  0.0815),
  TaxBracket(5108, 367.12,  0.0735),
  TaxBracket(20436,1493.71,  0.4902),
  TaxBracket(21459,1995.23,  0.0962),
)

# Based on the married table from nys-50-t-nys in comments above
nys_married_withholding_table = (
  #bracket_start, base_withholding, pct_of_excess
  TaxBracket(0, 0,  0.0400),
  TaxBracket(162, 6.46,  0.0450),
  TaxBracket(223, 9.23,  0.0525),
  TaxBracket(264, 11.40,  0.0590),
  TaxBracket(407, 19.79,  0.0645),
  TaxBracket(1531, 92.31,  0.0665),
  TaxBracket(1838, 112.69,  0.0728),
  TaxBracket(2042, 127.60,  0.0778),
  TaxBracket(3064, 207.13,  0.0808),
  TaxBracket(4087, 289.71,  0.0715),
  TaxBracket(6130, 435.81,  0.0815),
  TaxBracket(7152, 519.12,  0.0735),
  TaxBracket(20436, 1495.46,  0.0765),
  TaxBracket(40874, 3059.00,  0.8842),
  TaxBracket(41897, 3963.60,  0.0962),
)

def get_tax_bracket(taxable_income, bracket_table):

  # search from highest bracket downward
  for bracket in reversed(bracket_table):
    if bracket.bracket_start <= taxable_income:
      return bracket

  # less than lowest bracket - no tax owed
  return TaxBracket(0,0,0)


def get_bracket_table_and_deduction_amount(federal, married, number_of_allowances):

  if federal:
    deduction_amount = number_of_allowances*FEDERAL_WEEKLY_WITHHOLDING_ALLOWANCE
    if married:
      bracket_table = federal_married_withholding_table
    else: #single
      bracket_table = federal_single_withholding_table
  else: #NYS
    if married:
      bracket_table = nys_married_withholding_table
      deduction_amount = married_nys_deductions_ordered_by_number_of_allowances[number_of_allowances]
    else: #single
      bracket_table = nys_single_withholding_table
      deduction_amount = single_nys_deductions_ordered_by_number_of_allowances[number_of_allowances]

  return bracket_table, deduction_amount


def get_amount_to_withhold(federal, married, number_of_allowances, total_income):

  bracket_table, deduction_amount = get_bracket_table_and_deduction_amount(federal, married, number_of_allowances)

  taxable_income = total_income - deduction_amount
  bracket = get_tax_bracket(taxable_income, bracket_table)

  excess = taxable_income - bracket.bracket_start

  #federal pct is expresed as pct, state as decimal fraction
  #convert federal pct to fraction' leave state as is
  if federal: pct_of_excess = bracket.pct_of_excess/100.0
  else: pct_of_excess = bracket.pct_of_excess

  amount_to_with_hold = bracket.base_withholding + excess*pct_of_excess

  return amount_to_with_hold


def add_witholding_fields(employee_tax_info):
    try:
      eti = employee_tax_info #shorten name
      eti['fed_withholding'] = get_amount_to_withhold(True, eti['married'], eti['allowances'], eti['gross_wages'])
      eti['nys_withholding'] = get_amount_to_withhold(False, eti['married'], eti['allowances'], eti['gross_wages'])
      eti['social_security_tax'] = eti['gross_wages'] * SOCIAL_SECURITY_TAX_RATE
      eti['medicare_tax'] = eti['gross_wages'] *MEDICARE_TAX_RATE
    except TypeError as e:
      #e.message += str(employee_tax_info)
      raise Exception(str(employee_tax_info))



def populate_pay_stub():

  results = utils.select('''
  select
  DATE(intime) - interval (DAYOFWEEK(intime) -1) DAY as week_of,
  employee_tax_info.person_id,
  last_name, first_name,
  sum(hours_worked) as hours_worked,
  pay_rate, 
  allowances,
  nominal_scale,
  round(sum(hours_worked)*pay_rate) as weekly_pay,
  round(sum(hours_worked)*pay_rate*nominal_scale) as gross_wages,
  married,
  sum(tip_pay) tips,
  round(sum(hours_worked)*pay_rate - weekly_tax) + sum(tip_pay) as total_weekly,
  sum(tip_pay) / sum(hours_worked) + pay_rate as total_hourly_pay
  from hours_worked JOIN employee_tax_info ON hours_worked.person_id = employee_tax_info.person_id
  where yearweek(intime) = yearweek(now() - interval '1' week)
  and intime != 0
  group by employee_tax_info.person_id
  ''',
  incursor = None,
  label = True
  )

  for row in results:
    add_witholding_fields(employee_tax_info = row)
    columns = ','.join(row.keys())
    values = ','.join(map(str,row.values()))
    utils.execute('''INSERT into pay_stub (%s) VALUES (%s)'''%(columns, values))
    


def notuse():

  html = (
    '''  
      <html>
      <body>
    ''' +
    utils.tohtml(
      'Worked per week by person',
      results[0].keys(),
      results,
      breakonfirst = True
    ) +
    '''</body></html>'''
  )

  return html



if __name__ == '__main__':

  print '''
  From page 43 of IRS Publication 15 http://www.irs.gov/pub/irs-pdf/p15.pdf

  Example.   An unmarried employee is paid $800 weekly. This employee has in effect a Form W-4 claiming two withholding allowances. Using the percentage method, figure the income tax to withhold as follows:
  1.  Total wage payment      $800.00
  2.  One allowance   $76.90   
  3.  Allowances claimed on Form W-4  2    
  4.  Multiply line 2 by line 3       $153.80
  5   Amount subject to withholding (subtract line 4 from line 1)        
  $646.20
  6.  Tax to be withheld on $646.20 from Table 1—single person, page 45        
  $81.43 

  Code says:
  '''  
  print get_amount_to_withhold(federal = True, married = False, number_of_allowances = 2, total_income = 800)


  print '''
  Page 16 of 22 NYS-50-T-NYS (1/15) http://www.tax.ny.gov/pdf/publications/withholding/nys50_t_nys.pdf

                                    Example 1:                                
              Weekly payroll, $400 gross wages, single, 3 exemptions          
    1.	 Amount from Table A on page 14 is $199.10 for single, weekly payroll,
    	   3 exemptions. $400 wages - $199.10 = $200.90 net wages.              
    2.	 Use Table II - A on page 17 for single, weekly payroll. Look up      
    	   $200.90 and use line 2 on which $200.90 is greater than Column 1     
    	   ($162) but less than Column 2 ($223).                                
    3.	 $200.90 - $162 (from Column 3, line 2) = $38.90.                     
    4.	 $38.90 x .0450 (from Column 4, line 2) = $1.75.                      
    5.	 $1.75 + $6.46 (from Column 5, line 2) = $8.21. Withhold this amount. 
                                                                              
  Code says:
  '''
  print get_amount_to_withhold(federal = False, married = False, number_of_allowances = 3, total_income = 400)

  print '''
  Page 18 of 22 NYS-50-T-NYS (1/15) http://www.tax.ny.gov/pdf/publications/withholding/nys50_t_nys.pdf

                                    Example 1:                                
              Weekly payroll, $400 gross wages, married, 4 exemptions         

    1.	 Amount from Table A on page 14 is $227.95 for married, weekly        
    	   payroll, 4 exemptions. $400 wages - $227.95 = $172.05 net wages.     
    2.	 Use Table II - A on page 19 for married, weekly payroll. Look up     
    	   $172.05 and use line 2 on which $172.05 is greater than Column 1     
    	   ($162) but less than Column 2 ($223).                                
    3.	 $172.05 - $162 (from Column 3, line 2) = $10.05.                     
    4.	 $10.05 x .0450 (from Column 4, line 2) = $0.45.                      
    5.	 $0.45 + $6.46 (from Column 5, line 2) = $6.91. Withhold this amount. 
                                                                              
  Code says:
  '''
  print get_amount_to_withhold(federal = False, married = True, number_of_allowances = 4, total_income = 400)

  print get_amount_to_withhold(federal = False, married = True, number_of_allowances = 4, total_income = 700)
  print get_amount_to_withhold(federal = True, married = True, number_of_allowances = 4, total_income = 700)

