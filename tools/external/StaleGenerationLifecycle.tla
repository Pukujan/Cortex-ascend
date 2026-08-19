---- MODULE StaleGenerationLifecycle ----
EXTENDS Naturals, FiniteSets, Sequences

CONSTANTS MaxGeneration

VARIABLES currentGen, attempts

AttemptState == {"PENDING", "RUNNING", "COMPLETED", "ADMITTED", "REJECTED", "STALE", "REVOKED"}

TypeOk ==
  /\ currentGen \in 0..MaxGeneration
  /\ attempts \in [0..MaxGeneration -> AttemptState \cup {"NONE"}]

Init ==
  /\ currentGen = 0
  /\ attempts = [g \in 0..MaxGeneration |-> "NONE"]

StartAttempt(g) ==
  /\ g = currentGen
  /\ attempts[g] = "NONE"
  /\ attempts' = [attempts EXCEPT ![g] = "RUNNING"]
  /\ UNCHANGED currentGen

CompleteAttempt(g, outcome) ==
  /\ attempts[g] = "RUNNING"
  /\ outcome \in {"ADMITTED", "REJECTED", "STALE"}
  /\ (outcome = "ADMITTED" => g = currentGen)
  /\ attempts' = [attempts EXCEPT ![g] = outcome]
  /\ UNCHANGED currentGen

ReplaceBase ==
  /\ currentGen < MaxGeneration
  /\ currentGen' = currentGen + 1
  /\ attempts' = [g \in 0..MaxGeneration |->
        IF attempts[g] = "ADMITTED" /\ g < currentGen'
          THEN "STALE"
          ELSE attempts[g]]

Next ==
  \/ ReplaceBase
  \/ \E g \in 0..MaxGeneration :
        StartAttempt(g) \/ \E outcome \in {"ADMITTED", "REJECTED", "STALE"} : CompleteAttempt(g, outcome)

NoStaleAdmit ==
  \A g \in 0..MaxGeneration :
    (g < currentGen) => attempts[g] # "ADMITTED"

Spec == Init /\ [][Next]_<<currentGen, attempts>>
====
