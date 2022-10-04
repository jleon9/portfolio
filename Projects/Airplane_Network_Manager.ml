(* 

NOTE: Because some type, function and variable definitions are private intellectual property, they are not visible in this file.

*)



(* ------------------------------------------------------------------------*)
(* Q1 : Money in the Bank *)
(* ------------------------------------------------------------------------*)

let open_account (initial_pass: passwd) : bank_account = 
  let pw = ref initial_pass in
  let log_counter = ref 0 in
  let bl = ref 0 in
  
  {
    update_pass = (fun opw npw ->  
        if opw = !pw then (log_counter:=0; pw := npw) 
        else (log_counter := !log_counter+1; raise wrong_pass));
    
    retrieve = (fun opw amt -> 
        if opw = !pw then 
          if !log_counter < 5 then
            (
              log_counter:=0;
              if amt<0 then raise negative_amount
              else if amt > !bl then raise not_enough_balance
              else bl := !bl-amt
            )
                 
          else raise too_many_failures 
              
        else if !log_counter < 5 then (
          log_counter := !log_counter+1; 
          raise wrong_pass
        )
        else raise too_many_failures 
      );
    
    deposit = (fun opw amt -> 
        if opw = !pw then 
          if !log_counter < 5 then (
            log_counter:=0;
            if amt<0 then raise negative_amount
            else
              (bl := !bl+amt;
               log_counter:=0) 
          )
          else raise too_many_failures 
              
        else if !log_counter < 5 then (
          log_counter := !log_counter+1;
          raise wrong_pass
        )
        else raise too_many_failures 
      );
    show_balance = (fun opw -> 
        if opw = !pw then 
          if !log_counter < 5 then
            (log_counter:=0;!bl)
          else raise too_many_failures
              
        else if !log_counter < 5 then (
          log_counter := !log_counter+1;
          raise wrong_pass
        )
        else raise too_many_failures
      );
  }
;;
let a = open_account "123";;

(* ------------------------------------------------------------------------*)
(* Q2 : I Want to Travel *)
(* ------------------------------------------------------------------------*)
(* TODO: Write some tests for neighbours. Consider creating a graph first, and then writing your tests based on it *)

(* Reminder: If a test case requires multiple arguments, use a tuple:
let myfn_with_2_args_tests = [
  ((arg1, arg1), (expected_output))
]
*)

(* We've added a type annotation here so that the compiler can help
   you write tests of the correct form. *)
let g1 = {nodes=["B";"J";"D";"A";"R"; "S"]; 
          edges=[("B","J",5);("J","D",5);("D","A",5);("A","R",5);("R","B",5);
                 ("B","D",3);("B","A",3);("R","J",3);("R","D",3);("J","A",3)]
         } 
;;

let g2 = {nodes=["Paris";"Accra";"Jeddah"];
          edges=[("Paris","Accra",7);("Paris","Jeddah",7);
                 ("Accra","Jeddah",10);("Accra","Paris",10);
                 ("Jeddah","Accra",7)]
         }
;;

let neighbours_tests: ((string graph * string) * (string * weight) list) list = [
  ((g2,"Paris"), [("Accra",7);("Jeddah",7)]);
  ((g2,"Accra"), [("Jeddah",10);("Paris",10)]);
  ((g2,"Jeddah"), [("Accra",7)]); 
  ((g1,"B"), [("J",5);("D",3);("A",3)]); 
  ((g1,"B"), [("J",5);("D",3);("A",3)]);
  ((g1,"J"), [("A",3);("D",5)]);
  ((g1,"D"), [("A",5)]);
  ((g1,"A"), [("R",5)]);
  ((g1,"R"), [("B",5);("J",3);("D",3)]);
  ((g1,"S"), []) 
]
;;

(* TODO: Implement neighbours. *)
let neighbours (g: 'a graph) (vertex: 'a) : ('a * weight) list =
  let get_fst (v1,_,_) = v1 in
  let p str tp = get_fst tp = str in
  let elist = List.filter (p vertex) (g.edges) in
  let f tp = let (_,v2,w) = tp in (v2,w) in 
  List.map f elist
;;

(* TODO: Implement find_path. *)
let find_path (g: 'a graph) (a: 'a) (b: 'a) : ('a list * weight) =
  let length = ref 0 in 
  
  let rec aux_node (node: 'a * weight) (visited : 'a list) : ('a list * weight) = 
    let (v1,w) = node in 
    if v1 = b then (List.rev (v1::visited), !length+w)
    else if (List.mem v1 visited) then (length := !length+w; raise Fail) 
    else (length := !length+w; aux_list (neighbours g v1) (v1::visited)) 
    
  and aux_list (nodes: ('a * weight) list) (visited: 'a list) : ('a list * weight) = 
    match nodes with
    | [] ->  raise Fail (* fc *)
    | (v1,w)::t -> 
        try aux_node (v1,w) visited 
        with Fail -> (length := !length-w; aux_list t visited)
  in
  aux_list (neighbours g a) [a]
;;


(* TODO: Implement find_path'. *) 
let find_path' (g: 'a graph) (a: 'a) (b: 'a) : ('a list * weight) = 
  let length = ref 0 in
  
  let rec aux_node (node: 'a * weight) (visited : 'a list) fc sc : ('a list * weight)  = 
    let (v1,w) = node in 
    
    if v1 = b then sc ((visited@[v1]), !length+w)
        
    else if (List.mem v1 visited) then 
      (length := !length+w; fc ())   
           
    else 
      (length := !length+w;
       aux_list (neighbours g v1) (visited@[v1]) fc (fun (path,cost) -> 
           (path,cost)) )
    
  and aux_list (nodes: ('a * weight) list) (visited: 'a list) fc sc : ('a list * weight) =
    match nodes with
    | [] -> fc () (*fc *) 
    | (v1,w)::t ->
        (aux_node (v1,w) visited (fun () -> aux_list t visited fc sc) sc)
  in
  aux_node (a,0) [] (fun () -> raise Fail) (fun t -> t)
;;

(* TODO: Implement find_all_paths *)
let find_all_paths (g: 'a graph) (a: 'a) (b: 'a) : ('a list * weight) list =
  let length = ref 0 in 
  let paths = ref [] in 
  
  let rec aux_node (node: 'a * weight) (visited : 'a list) : ('a list * weight) list = 
    let (v1,w) = node in 
    if List.mem v1 visited then
      (length := !length + w; raise Fail)
      
    else if v1 = b then
      !paths@[(visited@[v1], !length+w)]
  
    else
      (length := !length+w;
       aux_list (neighbours g v1) (visited@[v1]))
    
  and aux_list (nodes: ('a * weight) list) (visited: 'a list) : ('a list * weight) list = 
    match nodes with
    | [] -> []
    | (v1,w)::t -> 
        try aux_node (v1,w) visited 
        with Fail -> (length := !length-w; aux_list t visited)
  in
  aux_node (a,0) []
;;

(* TODO: Implement find_longest_path *)
let find_longest_path (g: 'a graph) (a: 'a) (b: 'a) : ('a list * weight) option = 
  match (find_all_paths g a b) with
  | [] -> None
  | (p,w)::_ -> Some (p,w)
;;
